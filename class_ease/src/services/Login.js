import React, { useState } from "react";
import api from "./api";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

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
 * @property {Object} credentials - The user's login credentials.
 * @property {string} credentials.id - The user's ID.
 * @property {string} credentials.password - The user's password.
 * @property {Function} setCredentials - Function to update the user's credentials.
 * @property {string} warning - Warning message displayed on authentication failure.
 * @property {Function} setWarning - Function to update the warning message.
 * @property {Function} navigate - Function to navigate to different routes.
 */
const Login = () => {
  const [credentials, setCredentials] = useState({ id: "", password: "" });
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

  /**
   * @function handleChange
   * @description Handles changes to the input fields and updates the credentials state.
   * @param {Event} e - The input change event.
   * @returns {void}
   */
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
