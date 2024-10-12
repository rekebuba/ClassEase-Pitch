import React, { useState } from "react";
import "./styles/AdminManageStudents.css";
import AdminPanel from "../components/AdminPanel";
// import { useNavigate } from "react-router-dom";
import AdminHeader from "../components/AdminHeader";
import AdminTeachProfile from "./AdminTeachProfile";
import AdminTeachList from "./AdminTeachList";

const AdminManageStudents = () => {

    const [isOpen, setIsOpen] = useState(false);

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    const toggleProfile = () => {
        setIsOpen(false);
    }

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <AdminHeader />
                <AdminTeachList toggleDropdown={toggleDropdown} />
                <AdminTeachProfile isOpen={isOpen} toggleProfile={toggleProfile} />
            </main>
        </div>
    );
};

export default AdminManageStudents;
