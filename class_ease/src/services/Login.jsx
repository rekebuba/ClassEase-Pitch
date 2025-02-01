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
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
        <h2 className="text-2xl font-semibold text-center text-gray-800 mb-6">
          Login to your account
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="relative mb-5">
            <i className="fa fa-user absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
            <input
              type="text"
              name="id"
              placeholder="ID"
              value={id}
              onChange={(e) => setId(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500"
            />
          </div>
          <div className="relative mb-5">
            <i className="fa fa-lock absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500"
            />
          </div>
          {warning && (
            <p className="text-red-500 text-sm mb-4">{warning}</p>
          )}
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition-colors"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
