import React, { useState } from "react";
import "./styles/AdminManageStudents.css";
import AdminPanel from "../components/AdminPanel";
// import { useNavigate } from "react-router-dom";
import AdminHeader from "../components/AdminHeader";
import AdminTeachProfile from "./AdminTeachProfile";
import AdminTeachList from "./AdminTeachList";
import AssignTeacher from "./AdminAssignTeacher";

const AdminManageStudents = () => {

    const [isDetailOpen, setIsDetailOpen] = useState(false);
    const [isEditOpen, setIsEditOpen] = useState(false);
    const [teacherSummary, setTeacherSummary] = useState({});


    const toggleDropdown = (role) => {
        if (role === 'detail') {
            setIsDetailOpen(!isDetailOpen);
        }
        if (role === 'edit') {
            setIsEditOpen(!isEditOpen);
        }
    };

    const toggleDetailProfile = () => {
        setIsDetailOpen(false);
    }

    const toggleEditProfile = () => {
        setIsEditOpen(false);
    }

    const summary = (data) => {
        setTeacherSummary(data);
    }

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <AdminHeader />
                <AdminTeachList toggleDropdown={toggleDropdown} teacherSummary={summary} />
                <AdminTeachProfile isDetailOpen={isDetailOpen} toggleDetailProfile={toggleDetailProfile} teacherData={teacherSummary} />
                <AssignTeacher isEditOpen={isEditOpen} toggleEditProfile={toggleEditProfile} teacherData={teacherSummary} />
            </main>
        </div>
    );
};

export default AdminManageStudents;
