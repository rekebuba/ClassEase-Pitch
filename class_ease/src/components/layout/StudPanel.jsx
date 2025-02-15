import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaUserCircle } from "react-icons/fa";
import { Logout } from "@/features/auth";
import { studentApi } from '@/api';


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
   * @param {Function} fetchStudent - Fetches student data from the API.
   * @returns {Object} The student data fetched from the API.
   * @throws {Error} If there is an error fetching the student data.
   * @async
   * @function fetchStudent
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
    const fetchStudent = async () => {
      try {
        const response = await studentApi.getPanelData();
        setStudentData(response.data);
      } catch (error) {
        if (error.response && error.response.data && error.response.data['error']) {
          console.error(error.response.data['error']);
        }
        return;
      }
    };
    fetchStudent();
  }, []);

  /**
   * @function updateProfile
   * @description Navigates to the update profile route.
   */
  const updateProfile = () => {
    navigate("/student/update/profile");
  };

  return (
    <aside className="flex flex-col justify-between fixed mt-[4.6rem] h-full w-48 bg-white p-7 border-r border-gray-200">
      {/* Top Profile Section */}
      <div className="flex flex-col items-center space-y-4">
        <FaUserCircle className="w-16 h-16 text-gray-500 cursor-pointer" onClick={updateProfile} />
        <h3 className="mt-4 text-center text-xl font-semibold text-gray-800">{studentData.name} {studentData.father_name} {studentData.grand_father_name}</h3>
      </div>
      <Logout />
    </aside>
  );
};


export default StudentPanel;
