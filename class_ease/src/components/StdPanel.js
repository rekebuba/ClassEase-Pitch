import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUserCircle, FaCogs } from "react-icons/fa";
import api from '../services/api';


/**
 * StudentPanel component renders the sidebar for the student dashboard.
 * It fetches student data from the API and displays the student's profile information.
 * The component also provides options to update the profile and logout.
 *
 * @component
 * @example
 * return (
 *   <StudentPanel />
 * )
 *
 * @returns {JSX.Element} The rendered sidebar component.
 *
 * @function
 * @name StudentPanel
 *
 * @description
 * This component uses the `useNavigate` hook from `react-router-dom` to navigate between routes.
 * It also uses the `useState` and `useEffect` hooks from React to manage and fetch student data.
 */
const StudentPanel = () => {
  const navigate = useNavigate();
  const [studentData, setStudentData] = useState({});

  /**
   * @hook useEffect
   * @description Fetches student data from the API when the component mounts.
   * @param {Function} fetchAdmin - Fetches student data from the API.
   * @returns {Object} The student data fetched from the API.
   * @throws {Error} If there is an error fetching the student data.
   * @async
   * @function fetchAdmin
   * @description Fetches student data from the API and updates the state.
   * @returns {Object} The student data fetched from the API.
   * @throws {Error} If there is an error fetching the student data.
   * @param {Object} error - The error response from the API.
   * @param {Object} error.response - The response object from the API.
   * @param {Object} error.response.data - The data object from the API response.
   * @param {string} error.response.data['error'] - The error message from the API response.
   * @returns {undefined} Returns early if there is an error.
   */
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

  /**
   * @function handleLogout
   * @description Navigates to the logout route.
   */
  const handleLogout = () => {
    navigate('/logout');
  }

  /**
   * @function updateProfile
   * @description Navigates to the update profile route.
   */
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
