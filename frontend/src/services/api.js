import axios from "axios";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8001",
});

export const registerFace = (username, file) => {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("file", file);

  return API.post("/auth/register", formData);
};

export const loginFace = (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return API.post("/auth/login", formData);
};
