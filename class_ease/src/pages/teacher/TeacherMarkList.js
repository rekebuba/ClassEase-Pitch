import React, { useState, useEffect } from 'react';

const TeacherMarkList = () => {
    const [grades, setGrades] = useState([]);
    const [sections, setSections] = useState([]);
    const [semesters, setSemesters] = useState([]);
    const [selectedGrade, setSelectedGrade] = useState('');
    const [selectedSection, setSelectedSection] = useState('');
    const [selectedSemester, setSelectedSemester] = useState('');
    const [students, setStudents] = useState([]);
    const [scores, setScores] = useState({});
    const [isSubmitted, setIsSubmitted] = useState(false);

    useEffect(() => {
        const mockGrades = ['Grade 1', 'Grade 2', 'Grade 3'];
        const mockSections = ['A', 'B', 'C'];
        const mockSemesters = ['Semester 1', 'Semester 2'];
        setGrades(mockGrades);
        setSections(mockSections);
        setSemesters(mockSemesters);
    }, []);

    const fetchStudents = () => {
        // Fetch students based on selected grade, section, and semester
        const mockStudents = [
            { id: 1, name: 'John Doe', score: 75 },
            { id: 2, name: 'Jane Smith', score: 85 },
            { id: 3, name: 'Emily Johnson', score: 90 },
        ];
        setStudents(mockStudents);
        const initialScores = mockStudents.reduce((acc, student) => {
            acc[student.id] = student.score;
            return acc;
        }, {});
        setScores(initialScores);
    };

    const handleScoreChange = (studentId, newScore) => {
        setScores({ ...scores, [studentId]: newScore });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitted(true);
    };

    return (
        <div className="teacher-section">
            <h2>Manage Student Scores</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="grade">Select Grade</label>
                    <select
                        id="grade"
                        value={selectedGrade}
                        onChange={(e) => setSelectedGrade(e.target.value)}
                        required
                    >
                        <option value="">Select Grade</option>
                        {grades.map((grade, index) => (
                            <option key={index} value={grade}>
                                {grade}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="section">Select Section</label>
                    <select
                        id="section"
                        value={selectedSection}
                        onChange={(e) => setSelectedSection(e.target.value)}
                        required
                    >
                        <option value="">Select Section</option>
                        {sections.map((section, index) => (
                            <option key={index} value={section}>
                                {section}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label htmlFor="semester">Select Semester</label>
                    <select
                        id="semester"
                        value={selectedSemester}
                        onChange={(e) => setSelectedSemester(e.target.value)}
                        required
                    >
                        <option value="">Select Semester</option>
                        {semesters.map((semester, index) => (
                            <option key={index} value={semester}>
                                {semester}
                            </option>
                        ))}
                    </select>
                </div>
                <button type="button" className="fetch-students-btn" onClick={fetchStudents}>
                    Fetch Students
                </button>
            </form>

            {students.length > 0 && (
                <form onSubmit={handleSubmit}>
                    <h3>Student List</h3>
                    <table className="student-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Score</th>
                            </tr>
                        </thead>
                        <tbody>
                            {students.map((student) => (
                                <tr key={student.id}>
                                    <td>{student.name}</td>
                                    <td>
                                        <input
                                            type="number"
                                            value={scores[student.id]}
                                            onChange={(e) => handleScoreChange(student.id, e.target.value)}
                                            min="0"
                                            max="100"
                                            required
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <button type="submit" className="submit-scores-btn">
                        Submit Scores
                    </button>
                </form>
            )}

            {isSubmitted && <p className="success-message">Scores updated successfully!</p>}
        </div>
    );
};

export default TeacherMarkList;
