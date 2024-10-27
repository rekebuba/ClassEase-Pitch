import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";
import api from '../services/api';

const AdminPanel = () => {
    const navigate = useNavigate();
    const [adminData, setAdminData] = useState({});

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
