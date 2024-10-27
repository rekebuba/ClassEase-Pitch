import React, { useState } from "react";
import "../../styles/AdminManageStudents.css";
import TeacherPanel from "../../components/TeachPanel";
import TeacherHeader from "../../components/TeachHeader";
import TeacherStudentsList from "./TeacherStudentsList";
import TeacherPopupUpdateStudentScore from "./TeacherPopupUpdateStudentScore";

/**
 * TeacherManageStudents component
 * @component
 * @return {component} TeacherManageStudents
 * @example
 * return <TeacherManageStudents />
 */
const TeacherManageStudents = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [studentSummary, setStudentSummary] = useState({});

    /**
     * @function toggleDropdown
     * @description Toggles the dropdown
     * @returns {void}
     */
    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    /**
     * @function toggleAssessment
     * @description Toggles the assessment
     * @returns {void}
     */
    const toggleAssessment = () => {
        setIsOpen(false);
    }

    /**
     * @function summary
     * @description Sets the student summary
     * @param {object} data - student data
     * @returns {void}
     */
    const summary = (data) => {
        setStudentSummary(data);
    }

    return (
        <div className="admin-manage-container">
            <TeacherPanel />
            <main className="content">
                <TeacherHeader />
                <TeacherStudentsList toggleDropdown={toggleDropdown} studentSummary={summary} />
                <TeacherPopupUpdateStudentScore isOpen={isOpen} toggleAssessment={toggleAssessment} studentData={studentSummary} />
            </main>
        </div>
    );
};

export default TeacherManageStudents;
