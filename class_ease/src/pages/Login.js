import React, { useState } from "react";
import { login } from "../services/api";
import { useNavigate } from "react-router-dom";
import "./styles/Login.css";

function Login() {
  const [credentials, setCredentials] = useState({
    id: "",
    password: ""
  });
  const [warning, setWarning] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();

    try {
      const data = await login(credentials);
      navigate(`/${data.role}/dashboard`); // Redirect to dashboard
    } catch (error) {
      setWarning("id or password is not correct");
    }
  };

  return (
    // <div className="container">
      <div className="login-section">
        <div className="login-box">
          <h2>Login to your account</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <i className="fa fa-user" />
              <input
                type="text"
                placeholder="id"
                value={credentials.id}
                onChange={e =>
                  setCredentials({ ...credentials, id: e.target.value })}
              />
            </div>
            <div className="input-group">
              <i className="fa fa-lock" />
              <input
                type="password"
                placeholder="Password"
                value={credentials.password}
                onChange={e =>
                  setCredentials({ ...credentials, password: e.target.value })}
              />
            </div>
            <button type="submit" className="login-button">
              Login
            </button>
            <p className="warning">
              {warning}
            </p>
            <p className="forgot-password">Forgot Password?</p>
          </form>
        </div>
      </div>
    // </div>
    // <div>
    //   <h2>Login</h2>
    //   <form onSubmit={handleSubmit}>
    //     <input
    //       type="text"
    //       placeholder="id"
    //       value={credentials.id}
    //       onChange={e =>
    //         setCredentials({ ...credentials, id: e.target.value })}
    //     />
    //     <input
    //       type="password"
    //       placeholder="Password"
    //       value={credentials.password}
    //       onChange={e =>
    //         setCredentials({ ...credentials, password: e.target.value })}
    //     />
    //     <button type="submit">Login</button>
    //     <p className="warning">
    //       {warning}
    //     </p>
    //   </form>
    // </div>
  );
}

export default Login;
