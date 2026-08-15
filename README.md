# Face Authentication System 👤🔒

A modern, full-stack Face Authentication System built with React and FastAPI. This application allows users to register an account using their face, log in seamlessly by taking or uploading a photo of their face, and securely access a protected dashboard upon successful authentication. 

It leverages deep learning (FaceNet) to extract 512-dimensional facial feature vectors, ensuring robust and accurate facial matching.

---

## 🚀 Features

* **Face Registration:** Users can register an account by providing a username and a face image.
* **Face Login (Authentication):** Users log in purely by providing a face image, which is instantly matched against the database.
* **Smart Auto-Redirect Flow:** 
  * Registration automatically redirects to the Login screen upon success.
  * Login automatically redirects to the Secure Dashboard upon face match.
* **Secure Dashboard:** A protected route that validates session JWT tokens, preventing unauthorized access.
* **Premium UI/UX:** A clean, responsive, dark-navy and green themed interface built with custom React CSS and Google Fonts.
* **Vector Database (Milvus):** Designed to integrate with Milvus vector database for lightning-fast facial similarity search, with an automatic fallback to an in-memory database if Milvus is not running locally.

---

## 🛠️ Technology Stack

**Frontend:**
* React.js (Create React App)
* React Router v6 (for page navigation)
* Axios (for API communication)
* Vanilla CSS (Custom design system)

**Backend:**
* FastAPI (Python backend framework)
* Uvicorn (ASGI web server)
* PyMilvus (Vector Database client)
* OpenCV & Pillow (Image processing)
* PyJWT & Python-JOSE (Token generation & security)
* Deep Learning / FaceNet (Facial embedding extraction)

---

## 📂 Project Structure

```
Face Authentication System/
│
├── frontend/                 # React Frontend Application
│   └── src/                  
│       ├── .env              # Configures dev server port to 5173
│       └── src/              # Active Source Code
│           ├── App.jsx       # Routing & Navigation Layout
│           ├── index.css     # Global Stylesheet
│           ├── pages/        # Register, Login, and Dashboard components
│           └── services/     # Axios API connection setup
│
├── backend/                  # FastAPI Backend Application
│   ├── app/                  
│   │   ├── main.py           # FastAPI Entry point & CORS setup
│   │   ├── api/              # API Route Controllers (auth, debug)
│   │   ├── services/         # Business Logic (authentication, registration, facenet)
│   │   └── database/         # Milvus DB config & user mappings
│   ├── requirements.txt      # Python dependencies
│   └── streamlit_app.py      # Optional debug testing interface
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have the following installed on your machine:
* **Node.js & npm** (v14 or higher)
* **Python** (v3.8 or higher)

### 2. Backend Setup
Open a terminal and navigate to the `backend` directory to install the Python dependencies:

```bash
cd backend
pip install -r requirements.txt
```

*(Note: If you plan to use Milvus instead of the in-memory fallback, ensure your Milvus docker container is running on port `19530`).*

### 3. Frontend Setup
Open a separate terminal and navigate to the `frontend/src` directory to install the React dependencies:

```bash
cd frontend/src
npm install
```

---

## 💻 How to Run the Application

You must run the frontend and backend servers simultaneously in separate terminal windows.

### Terminal 1: Start the Backend Server
```bash
cd backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```
*The backend API will start on `http://localhost:8001`.*

### Terminal 2: Start the Frontend Server
```bash
cd frontend/src
npm start
```
*The React application will open automatically in your browser at `http://localhost:5173`.*

---

## 📖 How to Use the Application

1. **Register (`http://localhost:5173/register`):**
   * Enter your desired username.
   * Upload a clear photo of your face.
   * Click **Register**. The system will hash your username, extract your facial features into a 512D vector, and save it. You will be automatically redirected to Login.
2. **Login (`http://localhost:5173/login`):**
   * Upload a new photo of your face (or the same one to test).
   * Click **Login**. The system compares the features of this photo against the database. If they match, a JWT token is assigned to your browser session, and you are redirected to the Dashboard.
3. **Dashboard (`http://localhost:5173/dashboard`):**
   * You are securely logged in and greeted by name! Click **Logout** to clear your session token and exit.
