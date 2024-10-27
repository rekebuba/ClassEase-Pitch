import React, { useState } from "react";
import api from "./api";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

const Login = () => {
  const [credentials, setCredentials] = useState({ id: "", password: "" });
  const [warning, setWarning] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.get('/login', { params: credentials });
      if (response.status === 200) {
        localStorage.setItem("Authorization", response.data.access_token);
        navigate(`/${response.data.role}/dashboard`);
      }
    } catch (error) {
      setWarning("ID or password is incorrect");
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCredentials((prevCredentials) => ({
      ...prevCredentials,
      [name]: value,
    }));
  };

  return (
    <div className="login-section">
      <div className="login-box">
        <h2>Login to your account</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <i className="fa fa-user" />
            <input
              type="text"
              name="id"
              placeholder="ID"
              value={credentials.id}
              onChange={handleChange}
              required
            />
          </div>
          <div className="input-group">
            <i className="fa fa-lock" />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={credentials.password}
              onChange={handleChange}
              required
            />
          </div>
          {warning && <p className="warning">{warning}</p>}
          <button type="submit" className="login-button">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
