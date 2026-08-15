import React, { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function Dashboard() {
  const [token, setToken] = useState("");
  const [username, setUsername] = useState("");
  const [registeredCount, setRegisteredCount] = useState(null);
  
  // Chat state
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState("");
  const messagesEndRef = useRef(null);

  const navigate = useNavigate();

  useEffect(() => {
    // Read token immediately
    const t = localStorage.getItem("token");
    const u = localStorage.getItem("username") || "User";
    setToken(t);
    setUsername(u);
    
    // Initial greeting
    setMessages([
      { sender: "bot", text: `Hii ${u}! Welcome back. How can I help you today?` }
    ]);

    // Check for token updates periodically
    const pollInterval = setInterval(() => {
      const updatedToken = localStorage.getItem("token");
      const updatedUser = localStorage.getItem("username") || "User";
      setToken(updatedToken);
      setUsername(updatedUser);
    }, 500);

    // Listen for storage changes
    const handleStorageChange = () => {
      const updatedToken = localStorage.getItem("token");
      const updatedUser = localStorage.getItem("username") || "User";
      setToken(updatedToken);
      setUsername(updatedUser);
    };

    window.addEventListener("storage", handleStorageChange);

    // Check registrations count
    axios.get("http://localhost:8001/debug/registrations")
      .then(res => {
        const count = res.data.count || 0;
        setRegisteredCount(count);
      })
      .catch(() => setRegisteredCount(0));

    return () => {
      clearInterval(pollInterval);
      window.removeEventListener("storage", handleStorageChange);
    };
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    setToken("");
    navigate("/login");
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMsg = inputMessage.trim();
    const newMessages = [...messages, { sender: "user", text: userMsg }];
    setMessages(newMessages);
    setInputMessage("");

    // Simulate bot reply
    setTimeout(() => {
      let botReply = "I'm just a simple assistant, but I'm happy you're here!";
      const lowerMsg = userMsg.toLowerCase();
      
      if (lowerMsg.includes("hi") || lowerMsg.includes("hello")) {
        botReply = `Hii ${username}! Nice to chat with you. How's your day going?`;
      } else if (lowerMsg.includes("how are you")) {
        botReply = `I am doing great, ${username}! Thanks for asking. How are you doing?`;
      } else if (lowerMsg.includes("help")) {
        botReply = `Sure thing, ${username}. You're in the Face Authentication dashboard!`;
      }

      setMessages(prev => [...prev, { sender: "bot", text: botReply }]);
    }, 600);
  };

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div style={{ display: "flex", justifyContent: "center", width: "100%", paddingBottom: "30px" }}>
      {token ? (
        <div style={{ display: "flex", flexDirection: "column", gap: "20px", width: "100%", maxWidth: "800px", alignItems: "center" }}>
          {/* Logged In Dashboard Card */}
          <div className="card dashboard-card" style={{ width: "100%", maxWidth: "500px" }}>
            <div className="checkmark-container">
              <div className="checkmark-circle">
                <svg viewBox="0 0 52 52" className="checkmark-svg">
                  <path fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8" />
                </svg>
              </div>
            </div>
            <h2 className="dashboard-title">Welcome to Dashboard!</h2>
            <p className="dashboard-desc">You are successfully logged in as <strong>{username}</strong>.</p>
            
            <div className="dashboard-btn-wrapper">
              <button onClick={handleLogout} className="btn btn-green">
                Logout
              </button>
            </div>
          </div>

          {/* Chat Assistant Card */}
          <div className="card chat-card" style={{ width: "100%", maxWidth: "600px", padding: "0", overflow: "hidden", display: "flex", flexDirection: "column", height: "400px" }}>
            <div style={{ backgroundColor: "#2b2b2b", padding: "15px", borderBottom: "1px solid #444" }}>
              <h3 style={{ margin: 0, color: "#fff", fontSize: "1.1rem" }}>💬 AI Assistant</h3>
            </div>
            
            <div style={{ flex: 1, padding: "15px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "10px", backgroundColor: "#1e1e1e" }}>
              {messages.map((msg, idx) => (
                <div key={idx} style={{ 
                  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                  backgroundColor: msg.sender === "user" ? "#4a90e2" : "#333",
                  color: "#fff",
                  padding: "10px 15px",
                  borderRadius: msg.sender === "user" ? "15px 15px 0 15px" : "15px 15px 15px 0",
                  maxWidth: "80%",
                  wordWrap: "break-word",
                  boxShadow: "0 2px 5px rgba(0,0,0,0.2)"
                }}>
                  {msg.text}
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            <div style={{ padding: "15px", borderTop: "1px solid #444", backgroundColor: "#252525" }}>
              <form onSubmit={handleSendMessage} style={{ display: "flex", gap: "10px", margin: 0 }}>
                <input 
                  type="text" 
                  value={inputMessage} 
                  onChange={e => setInputMessage(e.target.value)} 
                  placeholder="Type a message..." 
                  style={{ flex: 1, padding: "10px 15px", borderRadius: "20px", border: "1px solid #555", backgroundColor: "#333", color: "#fff", outline: "none", margin: 0 }}
                />
                <button type="submit" className="btn btn-blue" style={{ borderRadius: "20px", padding: "10px 20px", margin: 0 }}>
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      ) : (
        /* Access Denied Card */
        <div className="card" style={{ textAlign: "center", maxWidth: "500px" }}>
          <div style={{ fontSize: "3rem", marginBottom: "15px" }}>🔒</div>
          <h2 className="card-title">Access Denied</h2>
          {registeredCount === 0 ? (
            <p style={{ color: "var(--text-muted)", marginBottom: "25px" }}>
              No users are registered in the system yet. Please register first.
            </p>
          ) : (
            <p style={{ color: "var(--text-muted)", marginBottom: "25px" }}>
              You must be logged in to view the dashboard page.
            </p>
          )}
          <button onClick={() => navigate("/login")} className="btn btn-blue">
            Go to Login
          </button>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
