import { useState } from "react";
import { TeacherHeader, TeacherPanel } from "@/components/layout";
import { TeacherStudentList, TeacherUpdateScore } from "@/features/teacher";
import { Toaster } from '@/components/ui/sonner';
import "../../styles/AdminManageStudents.css";


/**
 * TeacherManageStudents component
 * @component
 * @return {component} TeacherManageStudents
 * @example
 * return <TeacherManageStudents />
 */
const TeacherManageStudent = () => {
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
                    <TeacherStudentList toggleDropdown={toggleDropdown} studentSummary={summary} saveStudent={onSave} toggleSave={handelSaving} />
                    <TeacherUpdateScore isOpen={isOpen} toggleAssessment={toggleAssessment} studentData={studentSummary} onSave={handelSaving} />
                    <Toaster />
                </main>
            </div>
        </div>
    );
};

export default TeacherManageStudent;
