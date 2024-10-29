import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";
import axios from 'axios';

/**
 * Login component handles user authentication.
 * 
 * This component provides a form for users to input their ID and password,
 * and attempts to authenticate them by sending a request to the server.
 * If authentication is successful, the user is redirected to their respective dashboard.
 * If authentication fails, a warning message is displayed.
 * 
 * @component
 * @example
 * return (
 *   <Login />
 * )
 * 
 * @returns {JSX.Element} The rendered login component.
 * 
 * @function
 * @name Login
 * 
 * @property {string} id - The user's ID.
 * @property {string} password - The user's password.
 * @property {string} warning - Warning message displayed on authentication failure.
 * @property {Function} setWarning - Function to update the warning message.
 * @property {Function} navigate - Function to navigate to different routes.
 */
const Login = () => {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const [warning, setWarning] = useState("");
  const navigate = useNavigate();

  /**
   * @function handleSubmit
   * @description Handles form submission, sends login request to the server, and processes the response.
   * @param {Event} e - The form submission event.
   * @returns {void}
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setWarning(""); // Reset warning on new submission attempt

    try {
      const response = await axios.post('http://localhost:5000/api/v1/login', { id, password });
      if (response.status === 200) {
        localStorage.setItem("Authorization", response.data.access_token);
        navigate(`/${response.data.role}/dashboard`);
      }
    } catch (error) {
      setWarning("ID or password is incorrect");
    }
  };

  return (
    <div className="login-section">
      <div className="login-box">
        <h2>Login to your account</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group" style={{ marginBottom: '20px', position: 'relative' }}>
            <i className="fa fa-user" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: '#888' }} />
            <input
              type="text"
              name="id"
              placeholder="ID"
              value={id}
              onChange={(e) => setId(e.target.value)}
              required
            />
          </div>
          <div className="input-group" style={{ marginBottom: '20px', position: 'relative' }}>
            <i className="fa fa-lock" style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: '#888' }} />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
