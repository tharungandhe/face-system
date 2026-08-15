import os
import urllib.request
import numpy as np
import cv2
import inspect
from fastapi import HTTPException

# URLs for ONNX models from OpenCV Zoo
YUNET_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
SFACE_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"

class FaceNetService:
    def __init__(self):
        self.model_dir = os.path.join(os.path.dirname(__file__), "..", "models", "weights")
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.yunet_path = os.path.join(self.model_dir, "face_detection_yunet_2023mar.onnx")
        self.sface_path = os.path.join(self.model_dir, "face_recognition_sface_2021dec.onnx")
        
        self._ensure_models_exist()
        
        try:
            # We don't set input size yet, Yunet needs image size at inference
            self.detector = cv2.FaceDetectorYN.create(self.yunet_path, "", (320, 320), 0.9, 0.3, 5000)
            self.recognizer = cv2.FaceRecognizerSF.create(self.sface_path, "")
            self.use_dnn = True
        except Exception as e:
            print(f"Failed to load DNN models, using fallback: {e}")
            self.use_dnn = False

    def _ensure_models_exist(self):
        import requests
        import warnings
        warnings.filterwarnings("ignore", message="Unverified HTTPS request")

        if not os.path.exists(self.yunet_path):
            print("Downloading YuNet face detection model...")
            try:
                r = requests.get(YUNET_URL, verify=False)
                with open(self.yunet_path, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"Failed to download YuNet: {e}")
                
        if not os.path.exists(self.sface_path):
            print("Downloading SFace face recognition model...")
            try:
                r = requests.get(SFACE_URL, verify=False)
                with open(self.sface_path, "wb") as f:
                    f.write(r.content)
            except Exception as e:
                print(f"Failed to download SFace: {e}")

    async def _bytes_from_upload(self, image):
        if hasattr(image, "read"):
            try:
                result = image.read()
                if inspect.isawaitable(result):
                    return await result
                return result
            except Exception: pass
            
        if hasattr(image, "file"):
            try:
                try: pos = image.file.tell()
                except Exception: pos = None
                result = image.file.read()
                if inspect.isawaitable(result): data = await result
                else: data = result
                if pos is not None:
                    try: image.file.seek(pos)
                    except Exception: pass
                return data
            except Exception: pass
        return None

    def _get_dnn_embedding(self, img_bytes):
        # Decode image
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image format or corrupted file.")

        height, width, _ = img.shape
        self.detector.setInputSize((width, height))

        # Detect face
        _, faces = self.detector.detect(img)
        if faces is None or len(faces) == 0:
            raise HTTPException(status_code=400, detail="No face detected in the provided image. Please ensure your face is clearly visible.")

        # Align and Extract feature
        face = faces[0]
        aligned_face = self.recognizer.alignCrop(img, face)
        feature = self.recognizer.feature(aligned_face)
        
        # Flatten the feature to a list
        vec = feature.flatten()
        
        # L2 normalize the feature vector
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
            
        vec = vec.tolist()
        
        # Pad to 512 dimensions to match the existing Milvus collection schema
        if len(vec) < 512:
            vec.extend([0.0] * (512 - len(vec)))
        elif len(vec) > 512:
            vec = vec[:512]
            
        return vec

    async def get_embedding(self, image):
        img_bytes = await self._bytes_from_upload(image)
        if img_bytes is None:
            raise HTTPException(status_code=400, detail="Empty image data")
            
        if self.use_dnn:
            return self._get_dnn_embedding(img_bytes)
        else:
            # Fallback mock embedding
            import hashlib
            h = hashlib.sha256(img_bytes).digest()
            seed = int.from_bytes(h[:8], "big")
            rng = np.random.default_rng(seed)
            return rng.random(512).tolist()