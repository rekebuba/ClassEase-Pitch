import { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import { Button } from '@/components/ui/button';
import { sharedApi } from '@/api';
import { toast } from "sonner"
import ExamAssessmentReports from "./AdminExamAssessmentReports";
import CollapsibleTable from "./CollapsibleTable";


/**
 * StudentProfile component displays a detailed profile of a student including their personal information and performance overview.
 *
 * @component
 * @param {Object} props - The properties object.
 * @param {boolean} props.isProfileOpen - A flag indicating whether the profile popup is open or closed.
 * @param {function} props.toggleAssessment - A function to toggle the assessment view.
 * @param {function} props.closeProfile - A function to close the profile popup.
 * @param {Object} props.studentProfileSummary - An object containing the summary of the student's profile.
 * @param {string} props.studentProfileSummary.student_id - The ID of the student.
 * @param {string} props.studentProfileSummary.grade - The grade of the student.
 * @param {string} props.studentProfileSummary.pictureUrl - The URL of the student's picture.
 * @param {string} props.studentProfileSummary.name - The name of the student.
 * @param {string} props.studentProfileSummary.father_name - The father's name of the student.
 * @param {string} props.studentProfileSummary.grand_father_name - The grandfather's name of the student.
 * @param {string} props.studentProfileSummary.date_of_birth - The date of birth of the student in 'YYYY-MM-DD' format.
 * @param {string} props.studentProfileSummary.section - The section of the student.
 * @param {Object} props.assessmentSummary - An object containing the summary of the student's assessment.
 *
 * @returns {JSX.Element} The rendered StudentProfile component.
 */
const AdminStudentProfile = ({ isProfileOpen, toggleAssessment, closeProfile, studentProfileSummary }) => {
    const [allSubjects, setAllSubjects] = useState([]);
    const [studentAssessment, setStudentAssessment] = useState([]);
    const [studentReport, setStudentReport] = useState([]);
    const [student, setStudent] = useState({});

    /**
     * @function calculateAge
     * @param {string} birthday - The date of birth of the student in 'YYYY-MM-DD' format.
     * @returns {number} The age of the student.
     * @description Calculates the age of the student based on their date of birth.
     */
    function calculateAge(birthday) {
        // birthday should be in the format 'YYYY-MM-DD'
        const birthDate = new Date(birthday);
        const today = new Date();

        return today.getFullYear() - birthDate.getFullYear();

    }

    useEffect(() => {
        /**
         * @function lodeStudentSubjectList
         * @description Loads the list of subjects for the student.
         * @async
         * @returns {Promise<void>} The response data.
         * @throws {error} The error that was caught
         */
        const lodeStudentSubjectList = async () => {
            try {
                if (studentProfileSummary !== undefined && Object.keys(studentProfileSummary).length > 0) {
                    const response = await sharedApi.getStudentAssessment({
                        student_id: studentProfileSummary.student_id,
                        grade_id: studentProfileSummary.grade_id,
                        section_id: studentProfileSummary.section_id,
                        year: studentProfileSummary.year
                    });
                    setStudentAssessment(response.data.assessment);
                    setStudentReport(response.data.summary)
                }
            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    toast.error(error.response.data['error'], {
                        description: "Please try again later, if the problem persists, contact the administrator.",
                        style: { color: 'red' }
                    });
                } else {
                    toast.error("An unexpected error occurred.", {
                        description: "Please try again later, if the problem persists, contact the administrator.",
                        style: { color: 'red' }
                    });
                }
            }
        };
        lodeStudentSubjectList();
        setStudent(studentProfileSummary);
    }, [isProfileOpen, studentProfileSummary]);

    return (
        <div className={`popup-overlay ${isProfileOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container'>
                <div className="flex justify-between items-center p-2">
                    <h3 className='text-center text-lg font-bold'>student Summary</h3>
                    <Button
                        className='bg-opacity-0 text-black hover:bg-opacity-10 hover:text-red-400 hover:scale-150'
                        onClick={closeProfile}
                    >
                        <FaTimes size={24} />
                    </Button>
                </div>
                <div className="popup-profile-header">
                    <div className="popup-profile-picture">
                        <img src={student.pictureUrl} alt="Student" />
                    </div>
                    <div className="popup-profile-info">
                        <h2>{student.name} {student.father_name} {student.grand_father_name} </h2>
                        <p>Age: {calculateAge(student.date_of_birth)}</p>
                        <p>Grade: {student.grade}</p>
                        <p style={{ margin: 0 }}>Section: {student.section}</p>
                    </div>
                </div>

                <div className="popup-profile-content">
                    <h3>Performance Overview</h3>
                    <ExamAssessmentReports subjectSummary={allSubjects} />
                    <div className="list-head">
                        <h3>
                            <span>{`Academic Year: ${student.year}`}</span>
                            <span className="ml-5">{`Grade: ${student.grade}`}</span>
                            <span className="ml-5">{`Semester: ${student.semester}`}</span>
                        </h3>
                    </div>
                    {studentAssessment &&
                        (<CollapsibleTable studentAssessment={studentAssessment} studentReport={studentReport} />)
                    }
                </div>
            </div>
        </div>
    );
};


export default AdminStudentProfile;
