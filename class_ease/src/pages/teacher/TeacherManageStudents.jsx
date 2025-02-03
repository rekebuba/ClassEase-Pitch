import { useState } from "react";
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
    const [onSave, setOnSave] = useState(false);

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
    };

    /**
     * @function summary
     * @description Sets the student summary
     * @param {object} data - student data
     * @returns {void}
     */
    const summary = (data) => {
        setStudentSummary(data);
    };

    const handelSaving = (value) => {
        setOnSave(value);
    };

    return (
        <div className="min-h-screen flex flex-col">
            <TeacherHeader />
            <div className="flex flex-1">
                <TeacherPanel />
                <main className="flex-1 p-6 bg-gray-100 overflow-scroll">
                    <TeacherStudentsList toggleDropdown={toggleDropdown} studentSummary={summary} saveStudent={onSave} toggleSave={handelSaving} />
                    <TeacherPopupUpdateStudentScore isOpen={isOpen} toggleAssessment={toggleAssessment} studentData={studentSummary} onSave={handelSaving} />
                </main>
            </div>
        </div>
    );
};

export default TeacherManageStudents;
