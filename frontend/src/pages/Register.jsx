import React, { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { registerFace } from "../services/api";

function Register() {
  const [username, setUsername] = useState("");
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState(null);
  const [webcamActive, setWebcamActive] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  
  const navigate = useNavigate();

  const startWebcam = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      streamRef.current = stream;
      setWebcamActive(true);
      setCapturedImage(null);
      setFile(null);
    } catch (err) {
      console.error("Error accessing webcam:", err);
      setStatus({
        type: "error",
        title: "Webcam Error",
        desc: "Could not access the webcam. Please grant permission."
      });
    }
  };

  const stopWebcam = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setWebcamActive(false);
  };

  const capturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      canvas.toBlob((blob) => {
        const capturedFile = new File([blob], "webcam_capture.jpg", { type: "image/jpeg" });
        setFile(capturedFile);
        setCapturedImage(URL.createObjectURL(blob));
        stopWebcam();
      }, "image/jpeg");
    }
  };

  const retakePhoto = () => {
    setCapturedImage(null);
    setFile(null);
    startWebcam();
  };

  useEffect(() => {
    startWebcam();
    return () => stopWebcam();
  }, []);

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!username.trim()) {
      setStatus({ type: "error", title: "Missing Username", desc: "Please provide a username to register." });
      return;
    }
    if (!file) {
      setStatus({ type: "error", title: "Missing Image", desc: "Please capture a face image." });
      return;
    }

    try {
      const res = await registerFace(username, file);
      if (res.data && res.data.access_token) {
        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("username", username);
      }
      setStatus({ type: "success", title: "Registration successful!", desc: "User registered and face saved." });
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      const detail = err.response?.data?.detail;
      const connectionMessage = err.code === "ERR_NETWORK"
        ? "Could not connect to the backend server. Please make sure the API is running on http://localhost:8001."
        : "Could not connect to server or face not detected.";

      setStatus({
        type: "error",
        title: "Registration failed",
        desc: detail || connectionMessage
      });
    }
  };

  return (
    <div className="card">
      <h2 className="card-title">User Registration</h2>
      
      <form onSubmit={handleRegister}>
        <div className="form-group">
          <label className="form-label">Username</label>
          <input
            type="text"
            className="text-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label className="form-label">Live Face Scanner</label>
          
          <div className="webcam-container" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
            {capturedImage ? (
              <>
                <img src={capturedImage} alt="Captured" style={{ width: '100%', maxWidth: '300px', borderRadius: '8px' }} />
                <button type="button" className="btn" onClick={retakePhoto} style={{ backgroundColor: '#ff9800', width: '100%' }}>Retake Photo</button>
              </>
            ) : (
              <>
                <div style={{ position: 'relative', width: '100%', maxWidth: '300px', borderRadius: '8px', overflow: 'hidden', backgroundColor: '#000' }}>
                  <video ref={videoRef} autoPlay playsInline muted style={{ width: '100%', display: 'block' }} />
                  <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: '60%', height: '80%', border: '2px dashed rgba(255,255,255,0.5)', borderRadius: '50%' }}></div>
                </div>
                <canvas ref={canvasRef} style={{ display: 'none' }} />
                <button type="button" className="btn btn-blue" onClick={capturePhoto} disabled={!webcamActive} style={{ width: '100%' }}>Capture Face</button>
              </>
            )}
          </div>
        </div>

        <button type="submit" className="btn btn-green" style={{ width: '100%' }}>Register</button>
      </form>

      {status && (
        <div className={`alert alert-${status.type}`} style={{ marginTop: '20px' }}>
          <div className="alert-title">{status.title}</div>
          <div className="alert-desc">{status.desc}</div>
        </div>
      )}
    </div>
  );
}

export default Register;
