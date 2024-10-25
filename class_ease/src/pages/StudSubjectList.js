import React, { useState, useEffect } from "react";
import './styles/StudDashboard.css';
import './styles/Dashboard.css';
import Alert from "./Alert";
import api from "../services/api";

function SubjectList({ student, allSubjects, toggleDropdown, studentSummary }) {
    return (
        <section className="student-list">
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
                            <td>{subject.average}</td>
                            <td>{subject.rank || 'N/A'}</td>
                            <td>
                                <button
                                    className="detail-btn"
                                    onClick={() => {
                                        studentSummary(subject);
                                        toggleDropdown();
                                    }}
                                >
                                    Detail
                                </button>
                            </td>
                        </tr>
                    ))}
                    <tr className="summary-row">
                        <td colSpan="3">Total Average</td>
                        <td>{student.average_score}</td>
                        <td>Rank: {student.rank}</td>
                    </tr>
                </tbody>
            </table>
        </section>
    );
}

const StudentSubjectList = ({ toggleDropdown, studentSummary }) => {
    const [selectedGrade, setSelectedGrade] = useState(1);
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [gradeAssigned, setGradeAssigned] = useState([]);
    const [allSubjects, setAllSubjects] = useState([]);
    const [student, setStudent] = useState({});

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
            showAlert("warning", errorMessage);
        }
    };

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    const handleSemesterChange = (e) => {
        setSelectedSemester(parseFloat(e.target.value));
    };

    const handleGradeChange = (e) => {
        setSelectedGrade(parseFloat(e.target.value));
    };

    const fetchAssignedGrade = async () => {
        try {
            const response = await api.get('/student/assigned_grade');
            setGradeAssigned(response.data['grade']);
        } catch (error) {
            const errorMessage = error.response?.data?.error || "An unexpected error occurred.";
            showAlert("warning", errorMessage);
        }
    };

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
                toggleDropdown={toggleDropdown}
                studentSummary={studentSummary}
            />
        </div>
    );
};

export default StudentSubjectList;
