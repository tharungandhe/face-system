import React from "react";
import { BrowserRouter as Router, Routes, Route, NavLink, Navigate } from "react-router-dom";
import Register from "./pages/Register";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <Router>
      <div className="app-container">
        {/* Navigation Bar */}
        <nav className="navbar">
          <div className="navbar-logo">
            <NavLink to="/register" className="navbar-logo-link">
              Face Authentication System
            </NavLink>
          </div>
          <div className="navbar-links">
            <NavLink 
              to="/register" 
              className={({ isActive }) => isActive ? "navbar-link active" : "navbar-link"}
            >
              Register
            </NavLink>
            <NavLink 
              to="/login" 
              className={({ isActive }) => isActive ? "navbar-link active" : "navbar-link"}
            >
              Login
            </NavLink>
            <NavLink 
              to="/dashboard" 
              className={({ isActive }) => isActive ? "navbar-link active" : "navbar-link"}
            >
              Dashboard
            </NavLink>
          </div>
        </nav>

        {/* Page Content */}
        <main className="content">
          <Routes>
            <Route path="/" element={<Navigate to="/register" replace />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="*" element={<Navigate to="/register" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
