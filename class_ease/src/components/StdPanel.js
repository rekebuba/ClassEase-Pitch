import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUserCircle, FaCogs } from "react-icons/fa";
import api from '../services/api';


const StudentPanel = () => {
  const navigate = useNavigate();
  const [studentData, setStudentData] = useState({});

  useEffect(() => {
    const fetchAdmin = async () => {
      try {
        const response = await api.get('/student/dashboard');
        setStudentData(response.data);
      } catch (error) {
        if (error.response && error.response.data && error.response.data['error']) {
          console.error(error.response.data['error']);
        }
        return
      }
    };
    fetchAdmin();
  }, []);

  const handleLogout = () => {
    navigate('/logout');
  }

  const updateProfile = e => {
    navigate("/student/update/profile")
  }

  return (
    <aside className="sidebar">
      <div className="profile-section">
        <FaUserCircle className="profile-icon" />
        <h3>{studentData.name} {studentData.father_name} {studentData.grand_father_name}</h3>
        <p>Grade {studentData.grade} - Section {studentData.section}</p>
      </div>
      <nav className="menu">
        <ul>
          <li onClick={updateProfile}><FaCogs /> Update Profile</li>
          <li onClick={handleLogout}>
            <FaSignOutAlt /> Logout
          </li>
        </ul>
      </nav>
    </aside>
  );
};


export default StudentPanel;
