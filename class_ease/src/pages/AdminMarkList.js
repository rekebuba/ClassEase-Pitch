import React, { useState } from 'react';
import AdminPanel from "../components/AdminPanel";
import AdminHeader from "../components/AdminHeader";
import './styles/AdminDashboard.css'
import { FaPlus } from 'react-icons/fa';

const AdminCreateMarkList = () => {
    const subjectsList = [
        'Math',
        'Science',
        'History',
        'Geography',
        'English',
        'Physical Education',
        'Art',
        'Music'
    ];

    const [selectedGrade, setSelectedGrade] = useState('Grade 1');
    const [selectedSection, setSelectedSection] = useState([]);
    const [selectedSubjects, setSelectedSubjects] = useState([]);
    const [assignmentTypes, setAssignmentTypes] = useState([{ type: '', percentage: '' }]);
    const [selectedSemester, setSelectedSemester] = useState('Semester 1');
    const [schoolYear, setSchoolYear] = useState('2024/25');
    const [selectAll, setSelectAll] = useState(false);

    const handleGradeChange = (e) => setSelectedGrade(e.target.value);
    const handleSectionChange = (e) => {
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSection([...selectedSection, value]);
        } else {
            setSelectedSection(selectedSection.filter((section) => section !== value))
        }
    }
    const handleSubjectChange = (e) => {
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSubjects([...selectedSubjects, value]);
        } else {
            setSelectedSubjects(selectedSubjects.filter((subject) => subject !== value));
        }
    };
    const handleSelectAll = () => {
        if (selectAll) {
            setSelectedSubjects([]);
        } else {
            setSelectedSubjects(subjectsList);
        }
        setSelectAll(!selectAll);
    };

    const handleAssignmentChange = (index, field, value) => {
        const newAssignments = [...assignmentTypes];
        newAssignments[index][field] = value;
        setAssignmentTypes(newAssignments);
    };

    const addAssignmentType = () => {
        setAssignmentTypes([...assignmentTypes, { type: '', percentage: '' }]);
    };

    const handleSemesterChange = (e) => setSelectedSemester(e.target.value);
    const handleYearChange = (e) => setSchoolYear(e.target.value);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Logic for submitting the mark list creation
    };

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <AdminHeader />
                <div className="admin-create-marklist-container">
                    <h2>Create Students Mark List</h2>
                    <form onSubmit={handleSubmit} className="marklist-form">
                        <div className="grade-section">
                            <div className="form-group">
                                <label htmlFor="grade">Grade:</label>
                                <select id="grade" value={selectedGrade} onChange={handleGradeChange}>
                                    {Array.from({ length: 12 }, (_, i) => i + 1).map(grade =>
                                        <option key={grade} value={grade}>
                                            Grade {grade}
                                        </option>
                                    )}
                                </select>
                            </div>
                            <div className="form-group">
                                <label htmlFor="semester">Semester:</label>
                                <select id="semester" value={selectedSemester} onChange={handleSemesterChange}>
                                    <option>Semester 1</option>
                                    <option>Semester 2</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label htmlFor="schoolYear">School Year:</label>
                                <select id="schoolYear" value={selectedSection} onChange={handleYearChange}>
                                    <option>2024/25</option>
                                    <option>2023/24</option>
                                    <option>2022/23</option>
                                    <option>2021/22</option>
                                </select>
                            </div>
                        </div>

                        <div className="form-group subjects">
                            <label htmlFor="subjects">section:</label>
                            <div className="checkbox-group">
                                {['A', 'B', 'C'].map((section) => (
                                    <div className="subject-container">
                                        <label key={section}>
                                            <input
                                                type="checkbox"
                                                value={section}
                                                checked={selectedSection.includes(section)}
                                                onChange={handleSectionChange}
                                            />
                                            {section}
                                        </label>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="form-group subjects">
                            <label htmlFor="subjects">Subjects:
                                <input
                                    type="checkbox"
                                    checked={selectAll}
                                    onChange={handleSelectAll}
                                />
                            </label>
                            <div className="checkbox-group">
                                {subjectsList.map((subject) => (
                                    <div className="subject-container">
                                        <label key={subject}>
                                            <input
                                                type="checkbox"
                                                value={subject}
                                                checked={selectedSubjects.includes(subject)}
                                                onChange={handleSubjectChange}
                                            />
                                            {subject}
                                        </label>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="assignment-container">
                            <h3>Assignment Types:</h3>
                            {assignmentTypes.map((assignment, index) => (
                                <div className="assignment-row" key={index}>
                                    <input
                                        type="text"
                                        placeholder="Type"
                                        value={assignment.type}
                                        className="assignment-input"
                                        onChange={e => {
                                            const newAssignments = [...assignmentTypes];
                                            newAssignments[index].type = e.target.value;
                                            setAssignmentTypes(newAssignments);
                                        }}
                                    />
                                    <select
                                        value={assignment.percentage}
                                        className="assignment-select"
                                        onChange={e => {
                                            const newAssignments = [...assignmentTypes];
                                            newAssignments[index].percentage = e.target.value;
                                            setAssignmentTypes(newAssignments);
                                        }}
                                    >
                                        <option value="">Percentage</option>
                                        <option value="5%">5%</option>
                                        <option value="10%">10%</option>
                                        <option value="15%">15%</option>
                                        <option value="20%">20%</option>
                                        <option value="25%">25%</option>
                                        <option value="30%">30%</option>
                                        <option value="35%">35%</option>
                                        <option value="40%">40%</option>
                                        <option value="45%">45%</option>
                                        <option value="50%">50%</option>
                                        <option value="100%">100%</option>

                                        {/* Add more options as needed */}
                                    </select>
                                </div>
                            ))}
                            <button className="add-assignment-btn" onClick={addAssignmentType}>
                                <FaPlus /> Add Assignment
                            </button>
                        </div>


                        <button type="submit" className="submit-btn">Create Mark List</button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default AdminCreateMarkList;
