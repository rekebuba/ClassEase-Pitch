"use client"

import { useState } from 'react';
import { Layout } from "@/components";
import { FaPlus } from 'react-icons/fa';
import { adminApi } from "@/api";
import { toast } from "sonner"
import '../../styles/AdminDashboard.css';
import '../../styles/Table.css';

/**
 * AdminCreateMarkList component for creating a mark list for students.
 * 
 * @component
 * @returns {JSX.Element} The rendered component.
 * 
 * @example
 * return (
 *   <AdminCreateMarkList />
 * )
 * 
 * @description
 * This component allows an admin to create a mark list for students by selecting grade, semester, school year, sections, subjects, and assessment types. 
 * It includes functionalities to add new subjects, validate assessment percentages, and submit the mark list data to the server.
 * 
 * @function
 * @name AdminCreateMarkList
 * 
 * @property {Array<string>} subjectsList - List of predefined subjects.
 * @property {Array<number>} percentages - List of predefined percentages for assessments.
 * @property {Array<string>} subjects - State for managing the list of subjects.
 * @property {number} selectedGrade - State for managing the selected grade.
 * @property {Array<string>} selectedSection - State for managing the selected sections.
 * @property {Array<string>} selectedSubjects - State for managing the selected subjects.
 * @property {string} newCheckboxLabel - State for managing the label of a new subject checkbox.
 * @property {boolean} AddNewCheckbox - State for toggling the addition of a new subject checkbox.
 * @property {Array<Object>} assessmentTypes - State for managing the list of assessment types and their percentages.
 * @property {number} selectedSemester - State for managing the selected semester.
 * @property {string} schoolYear - State for managing the selected school year.
 * @property {boolean} selectAll - State for toggling the selection of all subjects.
 * @property {number} totalAssessment - State for managing the total percentage of assessments.
 * @property {number} currentYear - State for managing the current year.
 * @property {Object} alert - State for managing alert messages.
 */
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

    /**
     * @function handleGradeChange
     * @description Handles the change event for the grade selection.
     * @param {Event} e - The change event.
     */
    const handleGradeChange = (e) => {
        setSelectedGrade(parseFloat(e.target.value));
    };

    /**
     * @function handleSemesterChange
     * @description Handles the change event for the semester selection.
     * @param {Event} e - The change event.
     * @param {*} e 
     */
    const handleSemesterChange = (e) => {
        setSelectedSemester(parseFloat(e.target.value));
    };

    /**
    * @function handleSectionChange
    * @description Handles the change event for the section selection.
    * @param {Event} e - The change event.
     */
    const handleSectionChange = (e) => {
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSection([...selectedSection, value]);
        } else {
            setSelectedSection(selectedSection.filter((section) => section !== value));
        }
    };

    /**
     * @function handleSubjectChange
     * @description Handles the change event for the subject selection.
     * @param {Event} e - The change event. 
     */
    const handleSubjectChange = (e) => {
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSubjects([...selectedSubjects, value]);
        } else {
            setSelectedSubjects(selectedSubjects.filter((subject) => subject !== value));
        }
    };

    /** 
     * @function addCheckbox
     * @description Handles the addition of a new subject checkbox.
     * @param {Event} e - The click event.
     */
    const addCheckbox = (e) => {
        e.preventDefault();
        var modifiedLabel = newCheckboxLabel.trim();
        modifiedLabel = modifiedLabel.charAt(0).toUpperCase() + modifiedLabel.slice(1);
        if (modifiedLabel !== '' && !subjects.includes(modifiedLabel)) {
            setSubjects([...subjects, modifiedLabel]);
            setNewCheckboxLabel('');
        }
    };
    /** 
     * @function handleTotalAssessment
     * @description Calculates and sets the total percentage of assessments.
     */
    const handleTotalAssessment = () => {
        const totalPercentage = assessmentTypes.reduce((acc, { percentage }) => {
            return acc + (percentage ? parseFloat(percentage) : 0); // ensure it's a number
        }, 0);
        setTotalAssessment(totalPercentage);
    };

    /** 
     * @function handleValidAssessment
     * @description Validates if the total percentage of assessments is less than 100%.
     * @returns {boolean} True if valid, otherwise false.
     */
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
    };

    /** 
     * @function handleSelectAll
     * @description Toggles the selection of all subjects.
     */
    const handleSelectAll = () => {
        if (selectAll) {
            setSelectedSubjects([]);
        } else {
            setSelectedSubjects(subjectsList);
        }
        setSelectAll(!selectAll);
    };

    /**
     * @function addAssessmentType
     * @description Handles the addition of a new assessment type.
     * @param {Event} e - The click event.
     */
    const addAssessmentType = (e) => {
        e.preventDefault();
        // checks if at least one element in the array satisfies the condition
        const hasEmptyFields = assessmentTypes.some(({ type, percentage }) => type === '' || percentage === 0);

        if (!hasEmptyFields && handleValidAssessment()) {
            setAssessmentTypes([...assessmentTypes, { type: '', percentage: 0 }]);
        }
    };

    /**
     * @function handleYearChange
     * @description Handles the change event for the school year selection.
     * @param {Event} e - The change event.
     */
    const handleYearChange = (e) => {
        setSchoolYear(e.target.value);
    };

    /**
     * @function checkValidData
     * @description Validates the form data before submission.
     * @param {Event} e - The submit event.
     */
    const checkValidData = (e) => {
        e.preventDefault();
        if (selectedSection.length === 0) {
            toast.error("Please select at least one section.", {
                style: { color: 'red' }
            });
            return;
        } else if (selectedSubjects.length === 0) {
            toast.error("Please select at least one subject.", {
                style: { color: 'red' }
            });
            return;
        } else if (assessmentTypes.length < 1) {
            toast.error("Please add assessment.", {
                style: { color: 'red' }
            });
            return;
        } else if (totalAssessment !== 100) {
            toast.error("Total assessment percentage should be 100%.", {
                style: { color: 'red' }
            });
            return;
        }
        handleSubmit();
    };


    /**
     * @function handleSubmit
     * @description Submits the mark list data to the server.
     * @async
     * @returns {Promise<void>}
     */
    const handleSubmit = async () => {
        const markListData = {
            "grade": selectedGrade,
            "sections": selectedSection,
            "subjects": selectedSubjects,
            "assessment_type": assessmentTypes,
            "semester": selectedSemester,
            "year": schoolYear
        };
        try {
            const response = await adminApi.createMarkList(markListData);

            // If successful, show a success alert
            toast.success(response.data['message'], {
                description: currentTime,
                style: { color: 'green' }
            });
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

    return (
        <Layout role="admin">
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
                                        handleTotalAssessment(e);
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
                    </div>
                    <button type="submit" className="submit-btn">Create Mark List</button>
                </form>
            </div>
        </Layout>
    );
};

export default AdminCreateMarkList;
