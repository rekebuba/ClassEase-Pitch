import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";
import api from '../services/api';

/**
 * AdminPanel component renders the admin dashboard sidebar.
 * It fetches admin data from the server and displays the admin's profile information.
 * It also provides a logout option.
 *
 * @component
 * @example
 * return (
 *   <AdminPanel />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @function
 * @name AdminPanel
 *
 * @description
 * - Uses `useNavigate` from `react-router-dom` to navigate to the logout page.
 * - Uses `useState` to manage the admin data state.
 * - Uses `useEffect` to fetch admin data from the server when the component mounts.
 * - Displays the admin's profile information including name and role.
 * - Provides a logout option that navigates to the logout page.
 *
 * @dependencies
 * - `react`
 * - `react-router-dom`
 * - `react-icons/fa`
 * - `api` (assumed to be an instance of Axios or similar for making HTTP requests)
 */
const AdminPanel = () => {
    const navigate = useNavigate();
    const [adminData, setAdminData] = useState({});

    /**
     * @hook useEffect
     * @description Fetches admin data from the server when the component mounts.
     * @param {Function} fetchAdmin - Fetches admin data from the server.
     */
    useEffect(() => {
        const fetchAdmin = async () => {
            try {
                const response = await api.get('/admin/dashboard');
                setAdminData(response.data);
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
     * @description Navigates to the logout page.
     */
    const handleLogout = () => {
        navigate('/logout');
    }

    return (
        <aside className="sidebar">
            <div className="profile-section">
                <FaUserCircle className="profile-icon" />
                <h3>{adminData.__class__} Panel</h3>
                <p>Mr. {adminData.name}</p>
                <p>Principal</p>
            </div>
            <nav className="menu">
                <ul>
                    <li onClick={handleLogout}>
                        <FaSignOutAlt /> Logout
                    </li>
                </ul>
            </nav>
        </aside>
    );
};

export default AdminPanel;
