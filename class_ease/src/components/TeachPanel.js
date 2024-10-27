import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUserCircle } from "react-icons/fa";
import api from '../services/api';


const TeacherPanel = () => {
    const navigate = useNavigate();
    const [teacherData, setTeacherData] = useState({});

    useEffect(() => {
        const fetchAdmin = async () => {
            try {
                const response = await api.get('/teacher/dashboard');
                setTeacherData(response.data);
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
                <h3>{teacherData.__class__} Panel</h3>
                <p>Mr. {teacherData.first_name} {teacherData.last_name}</p>
                <p>{teacherData.subject_taught} Teacher</p>
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

export default TeacherPanel;
