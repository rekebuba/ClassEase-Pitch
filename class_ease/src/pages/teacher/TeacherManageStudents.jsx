import { useState } from "react";
import "../../styles/AdminManageStudents.css";
import TeacherPanel from "../../components/TeachPanel";
import TeacherHeader from "../../components/TeachHeader";
import TeacherStudentsList from "./TeacherStudentsList";
import TeacherPopupUpdateStudentScore from "./TeacherPopupUpdateStudentScore";
import { Toaster } from '@/components/ui/sonner';


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
        <div className="min-h-screen flex overflow-hidden flex-col">
            <TeacherHeader />
            <div className="flex flex-1 scroll-m-0">
            <TeacherPanel />
                <main className="flex-1 p-6 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    <TeacherStudentsList toggleDropdown={toggleDropdown} studentSummary={summary} saveStudent={onSave} toggleSave={handelSaving} />
                    <TeacherPopupUpdateStudentScore isOpen={isOpen} toggleAssessment={toggleAssessment} studentData={studentSummary} onSave={handelSaving} />
                    <Toaster />
                </main>
            </div>
        </div>
    );
};

export default TeacherManageStudents;
