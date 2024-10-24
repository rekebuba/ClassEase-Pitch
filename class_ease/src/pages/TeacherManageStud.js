import React, { useState } from "react";
import "./styles/AdminManageStudents.css";
import { FaSearch } from 'react-icons/fa';
import TeacherPanel from "../components/TeachPanel";
import TeacherHeader from "../components/TeachHeader";
import TeacherStudentsList from "./TeacherStudentsList";
import PopupTable from "./PopupTable";


const TeacherManageStudents = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [studentSummary, setStudentSummary] = useState({});

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    const toggleAssessment = () => {
        setIsOpen(false);
    }

    const summary = (data) => {
        setStudentSummary(data);
    }

    return (
        <div className="admin-manage-container">
            <TeacherPanel />
            <main className="content">
                <TeacherHeader />
                <TeacherStudentsList toggleDropdown={toggleDropdown} studentSummary={summary} />
                <PopupTable isOpen={isOpen} toggleAssessment={toggleAssessment} studentData={studentSummary} />
            </main>
        </div>
    );
};

export default TeacherManageStudents;
