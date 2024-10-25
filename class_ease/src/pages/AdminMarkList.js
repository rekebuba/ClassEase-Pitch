import React, { useState } from 'react';
import AdminPanel from "../components/AdminPanel";
import AdminHeader from "../components/AdminHeader";
import './styles/AdminDashboard.css'
import { FaPlus } from 'react-icons/fa';
import api from "../services/api";
import Alert from './Alert';

const AdminCreateMarkList = () => {
    const subjectsList = [
        'Math',
        'Science',
        'History',
        'Geography',
        'English',
        'Physical Education',
        'Art',
        'Music',
    ];
    const percentages = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100];

    const [subjects, setSubjects] = useState(subjectsList);
    const [selectedGrade, setSelectedGrade] = useState(1);
    const [selectedSection, setSelectedSection] = useState([]);
    const [selectedSubjects, setSelectedSubjects] = useState([]);
    const [newCheckboxLabel, setNewCheckboxLabel] = useState('');
    const [AddNewCheckbox, setAddNewCheckbox] = useState(false);
    const [assessmentTypes, setAssessmentTypes] = useState([{ type: '', percentage: 0 }]);
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [schoolYear, setSchoolYear] = useState('2024/25');
    const [selectAll, setSelectAll] = useState(false);
    const [totalAssessment, setTotalAssessment] = useState(0);
    const [currentYear] = useState(new Date().getFullYear());
    const [alert, setAlert] = useState({ type: "", message: "", show: false });

    const handleGradeChange = (e) => {
        setSelectedGrade(parseFloat(e.target.value));
    }

    const handleSemesterChange = (e) => {
        setSelectedSemester(parseFloat(e.target.value));
    }

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

    // Handle adding a new checkbox
    const addCheckbox = (e) => {
        e.preventDefault();
        var modifiedLabel = newCheckboxLabel.trim()
        modifiedLabel = modifiedLabel.charAt(0).toUpperCase() + modifiedLabel.slice(1);
        if (modifiedLabel !== '' && !subjects.includes(modifiedLabel)) {
            setSubjects([...subjects, modifiedLabel]);
            setNewCheckboxLabel('');
        }
    };

    const handleTotalAssessment = (e) => {
        const totalPercentage = assessmentTypes.reduce((acc, { percentage }) => {
            return acc + (percentage ? parseFloat(percentage) : 0); // ensure it's a number
        }, 0);
        setTotalAssessment(totalPercentage);
    }

    const handleValidAssessment = () => {
        // Calculate sum using reduce
        const totalPercentage = assessmentTypes.reduce((acc, { percentage }) => {
            return acc + (percentage ? parseFloat(percentage) : 0); // ensure it's a number
        }, 0);
        if (totalPercentage >= 100) {
            return false;
        } else {
            return true;
        }
    }

    const handleSelectAll = () => {
        if (selectAll) {
            setSelectedSubjects([]);
        } else {
            setSelectedSubjects(subjectsList);
        }
        setSelectAll(!selectAll);
    };

    const addAssessmentType = (e) => {
        e.preventDefault();
        // checks if at least one element in the array satisfies the condition
        const hasEmptyFields = assessmentTypes.some(({ type, percentage }) => type === '' || percentage === 0);

        if (!hasEmptyFields && handleValidAssessment()) {
            setAssessmentTypes([...assessmentTypes, { type: '', percentage: 0 }]);
        }
    };

    const handleYearChange = (e) => {
        setSchoolYear(e.target.value);
    }

    const checkValidData = (e) => {
        e.preventDefault()
        if (selectedSection.length === 0) {
            showAlert("warning", "Please select at least one section.");
            return;
        } else if (selectedSubjects.length === 0) {
            showAlert("warning", "Please select at least one subject.");
            return;
        } else if (assessmentTypes.length < 1) {
            showAlert("warning", "Please add assessment.");
            return;
        } else if (totalAssessment !== 100) {
            showAlert("warning", "Total assessment percentage should be 100%.");
            return;
        }
        handleSubmit();
    }

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    const handleSubmit = async () => {
        // Logic for submitting the mark list creation
        const mark_list_data = {
            "grade": selectedGrade,
            "sections": selectedSection,
            "subjects": selectedSubjects,
            "assessment_type": assessmentTypes,
            "semester": selectedSemester,
            "year": schoolYear
        }
        console.log(mark_list_data)
        try {
            const response = await api.put('admin/students/mark_list', mark_list_data)
            console.log(response.data)

            // If successful, show a success alert
            showAlert("success", "Mark list created successfully!");
        } catch (error) {
            // setAlert({ type: "success", message: "success", show: true });
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
            } else {
                showAlert("warning", "An unexpected error occurred.");
            }
        }
    };

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <AdminHeader />
                <div className="admin-create-marklist-container">
                    <h2>Create Students Mark List</h2>
                    <form onSubmit={(e) => checkValidData(e)} className="marklist-form">
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
                                    {Array.from({ length: 2 }, (_, i) => i + 1).map(semester =>
                                        <option key={semester} value={semester}>
                                            Semester {semester}
                                        </option>
                                    )}
                                </select>
                            </div>
                            <div className="form-group">
                                <label htmlFor="schoolYear">School Year:</label>
                                <select id="schoolYear" value={schoolYear} onChange={handleYearChange}>
                                    {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                                        <option key={year} value={year}>
                                            {year}/{(year + 1) % 100}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className="form-group subjects">
                            <label htmlFor="section">Section:</label>
                            <div className="checkbox-group">
                                {['A', 'B', 'C'].map((section) => (
                                    <div className="subject-container" key={section}>
                                        <label>
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
                                {subjects.map((subject) => (
                                    <div className="subject-container" key={subject}>
                                        <label>
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
                                {/* Plus Icon Button */}
                                {!AddNewCheckbox &&
                                    <button
                                        onClick={() => setAddNewCheckbox(true)}
                                        style={{ fontSize: '15px', marginBottom: '20px', marginLeft: '10px' }}
                                    >
                                        <FaPlus /> Add
                                    </button>}
                            </div>
                            {AddNewCheckbox &&
                                <div className="add-checkbox">
                                    <input
                                        type="text"
                                        value={newCheckboxLabel}
                                        onChange={(e) => setNewCheckboxLabel(e.target.value)}
                                        placeholder="New subject"
                                    />
                                    <button onClick={(e) => addCheckbox(e)}>Add Subject</button>
                                    <button onClick={() => setAddNewCheckbox(false)}>Cancel</button>
                                </div>}
                        </div>

                        <div className="assessment-container">
                            <h3>Assessment Types:&nbsp;
                                <span style={{ color: totalAssessment > 100 ? "red" : totalAssessment === 100 ? "green" : "" }}>
                                    {totalAssessment}%
                                </span>
                            </h3>
                            {assessmentTypes.map((assessment, index) => (
                                <div className="assessment-row" key={index}>
                                    <select
                                        type="text"
                                        placeholder="Type"
                                        value={assessment.type}
                                        className="assessment-input"
                                        required
                                        onChange={e => {
                                            const newAssessments = [...assessmentTypes];
                                            newAssessments[index].type = e.target.value;
                                            setAssessmentTypes(newAssessments);
                                        }}
                                    >
                                        <option key={index} value="">Type</option>
                                        <option key={index} value="Test 1">Test 1</option>
                                        <option key={index} value="Test 2">Test 2</option>
                                        <option key={index} value="Test 3">Test 3</option>
                                        <option key={index} value="Quiz">Quiz</option>
                                        <option key={index} value="Attendance">Attendance</option>
                                        <option key={index} value="Mid Exam">Mid Exam</option>
                                        <option key={index} value="Final Exam">Final Exam</option>
                                        <option key={index} value="Model">Model</option>
                                    </select>
                                    <select
                                        value={assessment.percentage}
                                        className="assessment-select"
                                        required
                                        onChange={e => {
                                            const newAssessments = [...assessmentTypes];
                                            newAssessments[index].percentage = parseFloat(e.target.value);
                                            setAssessmentTypes(newAssessments);
                                            handleTotalAssessment(e)
                                        }}
                                    >
                                        <option value="">Percentage</option>
                                        {
                                            percentages.map((percentage) => (
                                                <option key={percentage} value={percentage}>{percentage}%</option>
                                            ))
                                        }
                                    </select>
                                </div>
                            ))}
                            <button className="add-assessment-btn" onClick={addAssessmentType}>
                                <FaPlus /> Add Assessment
                            </button>
                            <Alert
                                type={alert.type}
                                message={alert.message}
                                show={alert.show}
                                onClose={closeAlert}
                            />
                        </div>
                        <button type="submit" className="submit-btn">Create Mark List</button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default AdminCreateMarkList;
