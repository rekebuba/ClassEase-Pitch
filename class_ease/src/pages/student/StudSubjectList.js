import React, { useState, useEffect } from "react";
import '../../styles/StudDashboard.css';
import '../../styles/Table.css'
import '../../styles/Dashboard.css';
import Alert from "../../services/Alert";
import api from "../../services/api";

export function SubjectList({ student, allSubjects, toggleAssessment, assessmentSummary }) {
    return (
        <section className="table-section">
            <div className="list-head">
                {student.year && (
                    <h3>
                        <span>{`Academic Year: ${student.year}`}</span>
                        <span style={{ marginLeft: '20px' }}>{`Grade: ${student.grade}`}</span>
                        <span style={{ marginLeft: '20px' }}>{`Semester: ${student.semester}`}</span>
                    </h3>
                )}
            </div>

            <table className="data-table">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Subject</th>
                        <th>Average</th>
                        <th>Rank</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {allSubjects.map((subject, index) => (
                        <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                            <td>{index + 1}</td>
                            <td>{subject.subject}</td>
                            <td>{subject.subject_average}</td>
                            <td>{subject.rank || 'N/A'}</td>
                            <td>
                                <button
                                    className="detail-btn"
                                    onClick={() => {
                                        assessmentSummary(subject);
                                        toggleAssessment();
                                    }}
                                >
                                    Detail
                                </button>
                            </td>
                        </tr>
                    ))}
                    <tr className="summary-row">
                        <td colSpan="3">Total Average</td>
                        <td>{student.semester_average}</td>
                        <td>Rank: {student.rank}</td>
                    </tr>
                </tbody>
            </table>
        </section>
    );
}

/**
 * Component for displaying the list of subjects for a student.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.toggleAssessment - Function to toggle the assessment view.
 * @param {Object} props.assessmentSummary - Summary of the student's assessments.
 * @returns {JSX.Element} The rendered component.
 *
 * @example
 * <StudentSubjectList
 *   toggleAssessment={toggleAssessmentFunction}
 *   assessmentSummary={assessmentSummaryObject}
 * />
 *
 * @typedef {Object} Alert
 * @property {string} type - The type of alert (e.g., "warning", "success").
 * @property {string} message - The alert message.
 * @property {boolean} show - Whether the alert is visible.
 *
 * @typedef {Object} Student
 * @property {string} name - The name of the student.
 * @property {number} id - The ID of the student.
 */
const StudentSubjectList = ({ toggleAssessment, assessmentSummary }) => {
    const [selectedGrade, setSelectedGrade] = useState(1);
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [gradeAssigned, setGradeAssigned] = useState([]);
    const [allSubjects, setAllSubjects] = useState([]);
    const [student, setStudent] = useState({});

    /**
     * @function handleSearch
     * @description Handles the search for student scores based on the selected grade and semester.
     * @async
     * @returns {Promise<void>} A promise that resolves when the search is complete.
     * @throws {Error} An error if the search fails.
     * @throws {string} An error message if the search fails.
     * @throws {Object[]} An array of subjects if the search is successful.
     */
    const handleSearch = async () => {
        try {
            const response = await api.get('/student/score', {
                params: {
                    grade: selectedGrade,
                    semester: selectedSemester,
                }
            });

            setAllSubjects(response.data['student_assessment']);
            setStudent(response.data['student']);
        } catch (error) {
            const errorMessage = error.response?.data?.error || "An unexpected error occurred.";
            setAllSubjects([]);
            setStudent({});
            showAlert("warning", errorMessage);
        }
    };

    /**
     * @function showAlert
     * @description Sets the alert message and type.
     * @param {string} type - The type of alert (e.g., "warning", "success").
     * @param {string} message - The alert message.
     * @returns {void}
     */
    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    /**
     * @function closeAlert
     * @description Closes the alert.
     * @returns {void}
     */
    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    /**
     * @function handleSemesterChange
     * @description Handles the change in semester selection.
     * @param {Event} e - The semester change event.
     * @returns {void}
     */
    const handleSemesterChange = (e) => {
        setSelectedSemester(parseFloat(e.target.value));
    };

    /**
     * @function handleGradeChange
     * @description Handles the change in grade selection.
     * @returns {void}
     */
    const handleGradeChange = (e) => {
        setSelectedGrade(parseFloat(e.target.value));
    };

    /**
     * @function fetchAssignedGrade
     * @description Fetches the assigned grade for the student.
     * @async
     * @returns {Promise<void>} A promise that resolves when the grade is fetched.
     * @throws {Error} An error if the grade fetch fails.
     * @throws {string} An error message if the grade fetch fails.
     * @throws {number[]} An array of assigned grades if the fetch is successful.
     */
    const fetchAssignedGrade = async () => {
        try {
            const response = await api.get('/student/assigned_grade');
            setGradeAssigned(response.data['grade']);
        } catch (error) {
            const errorMessage = error.response?.data?.error || "An unexpected error occurred.";
            showAlert("warning", errorMessage);
        }
    };

    /**
     * @hook useEffect
     * @description Fetches the assigned grade when the component mounts.
     */
    useEffect(() => {
        fetchAssignedGrade();
    }, [selectedGrade]);

    return (
        <div className="dashboard-container">
            <section className="admin-filters">
                <div className="filter-group">
                    <label htmlFor="grade">Grade:</label>
                    <select
                        id="grade"
                        value={selectedGrade}
                        onChange={handleGradeChange}
                    >
                        {gradeAssigned.map((grade) => (
                            <option key={grade} value={grade}>
                                Grade {grade}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="filter-group">
                    <label htmlFor="semester">Semester:</label>
                    <select
                        id="semester"
                        value={selectedSemester}
                        onChange={handleSemesterChange}
                    >
                        {[1, 2].map((semester) => (
                            <option key={semester} value={semester}>
                                Semester {semester}
                            </option>
                        ))}
                    </select>
                </div>
                <button
                    className="filter-group-search"
                    onClick={handleSearch}
                >
                    Search
                </button>
            </section>
            <Alert
                type={alert.type}
                message={alert.message}
                show={alert.show}
                onClose={closeAlert}
            />
            <SubjectList
                allSubjects={allSubjects}
                student={student}
                toggleAssessment={toggleAssessment}
                assessmentSummary={assessmentSummary}
            />
        </div>
    );
};

export default StudentSubjectList;
