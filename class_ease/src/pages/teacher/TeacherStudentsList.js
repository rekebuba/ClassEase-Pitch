import { useState, useEffect, useCallback } from "react";
import { FaSearch } from 'react-icons/fa';
import Pagination from '../library/pagination';
import api from "../../services/api";
import Alert from '../../services/Alert';

function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, toggleDropdown, studentSummary }) {
    return (
        <section className="table-section">
            {(filteredStudents && filteredStudents.students && filteredStudents.students.length > 0) && (
                <form onSubmit={handleSearch}>
                    <div className="table-head">
                        <h3>Student List</h3>
                        <h3>
                            <span>{`Academic Year: ${filteredStudents.header.year}`}</span>
                            <span style={{ marginLeft: '20px' }}>{`Grade: ${filteredStudents.header.grade}`}</span>
                            <span style={{ marginLeft: '20px' }}>{`Subject: ${filteredStudents.header.subject}`}</span>
                        </h3>
                        <div className="table-search-bar">
                            <input
                                type="text"
                                placeholder="Search Student"
                                value={searchTerm}
                                onChange={handleSearchChange}
                                required
                            />
                            <button><FaSearch /></button>
                        </div>
                    </div>
                </form>
            )}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Father Name</th>
                        <th>G.Father Name</th>
                        <th>Section</th>
                        <th>Total Score</th>
                        <th>Rank</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {(filteredStudents && filteredStudents.students) &&
                        filteredStudents.students.map((student, index) => (
                            // Dynamic Data Rows
                            <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                                <td>{student.student_id}</td>
                                <td>{student.name}</td>
                                <td>{student.father_name}</td>
                                <td>{student.grand_father_name}</td>
                                <td>{student.section ? student.section : 'N/A'}</td>
                                <td>{student.total_score ? student.total_score : 0}</td>
                                <td>{student.rank ? student.rank : 0}</td>
                                <td>
                                    <button className="detail-btn" onClick={() => {
                                        toggleDropdown();
                                        studentSummary(student); // Pass the data for the clicked student
                                    }}>Detail</button>
                                </td>
                            </tr>
                        ))}
                </tbody>
            </table>
        </section >
    );
}


/**
 * TeacherStudentsList component for managing and displaying a list of students.
 * 
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.toggleDropdown - Function to toggle dropdown visibility.
 * @param {Object} props.studentSummary - Summary information about students.
 * 
 * @returns {JSX.Element} The rendered component.
 * 
 * @example
 * <TeacherStudentsList toggleDropdown={toggleDropdown} studentSummary={studentSummary} />
 * 
 * @description
 * This component allows teachers to manage and filter a list of students based on various criteria such as grade, section, semester, and year. It also provides search functionality and pagination for navigating through the list of students.
 */
const TeacherStudentsList = ({ toggleDropdown, studentSummary, saveStudent }) => {
    const [selectedGrade, setSelectedGrade] = useState('');
    const [selectedSubjectId, setSelectedSubjectId] = useState('');
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [selectedYear, setSelectedYear] = useState("2024/25");
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [allStudents, setAllStudents] = useState({ students: [], header: {} });        // Store all students
    const [filteredStudents, setFilteredStudents] = useState({ students: [], meta: {}, header: {} });  // Store the filtered search results
    const [selectedSection, setSelectedSection] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [currentYear] = useState(new Date().getFullYear());
    const [subjectAssigned, setSubjectAssigned] = useState([]);
    const [gradeAssigned, setGradeAssigned] = useState([]);
    const limit = 10; // Number of students per page

    /**
     * @function handleSearch
     * @description Fetches and filters the list of students based on the selected criteria and search term.
     * @param {number} [page] - The page number to fetch. If not provided, the current page is used.
     * @returns {void}
     */
    const handleSearch = async (e, page) => {
        e?.preventDefault(); // Prevent default if event exists
        setFilteredStudents({ students: [], meta: {}, header: {} }); // clear any search result for the new one
        setSearchTerm("");
        if (selectedSection.length === 0) {
            showAlert("warning", "Please select at least one section.");
            return;
        }
        page = page || currentPage; // If page is not provided, use the current page
        try {
            const response = await api.get('/teacher/students/mark_list', {
                params: {
                    subject_id: selectedSubjectId,
                    grade: selectedGrade,
                    year: selectedYear,
                    sections: selectedSection.join(','), // Convert array to comma-separated string
                    semester: selectedSemester,
                    page: page,
                    limit: limit,
                    search: searchTerm
                }
            });

            const data = {
                students: response.data['students'],
                meta: response.data['meta'],
                header: response.data['header']
            };

            if (searchTerm) {
                setFilteredStudents(data); // Update with search results
            } else {
                setAllStudents(data);      // Store all students
                setFilteredStudents(data); // Initially, filtered is the same as all
            }
            setCurrentPage(page);
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
            } else {
                showAlert("warning", "An unexpected error occurred.");
            }
            // Reset the state
            setCurrentPage(1);
            setFilteredStudents({ students: [], meta: {}, header: {} });
        }
    };

    // if (saveStudent) {
    //     handleSearch(undefined, currentPage);
    // }


    // useEffect(() => {
    //     if (saveStudent) {
    //         handleSearch(undefined, currentPage);
    //     }
    // }, [currentPage, saveStudent, handleSearch]);

    // Handle Next Page
    const handleNextPage = (e) => {
        if (currentPage < filteredStudents.meta.total_pages) {
            const newPage = currentPage + 1;  // Increment the page
            handleSearch(e, newPage);
        }
    };

    // Handle Previous Page
    const handlePreviousPage = (e) => {
        if (currentPage > 1) {
            const newPage = currentPage - 1;  // Decrement the page
            handleSearch(e, newPage);
        }
    };

    /**
     * @function showAlert
     * @description Displays an alert message.
     * @param {string} type - The type of alert (e.g., "warning").
     * @param {string} message - The alert message.
     * @returns {void}
     */
    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    /**
     * @function closeAlert
     * @description Closes the alert message.
     * @returns {void}
     */
    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    /**
     * @function handleGradeChange
     * @description Handles changes to the selected grade.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleGradeChange = (e) => {
        if (e.target.value === '') {
            setSelectedGrade(e.target.value);
        } else {
            setFilteredStudents({ students: [], meta: {}, header: {} }); // clear any search result for the new one
            setSearchTerm("");
            const value = e.target.value.replace(/\D/g, ""); // Keep only digits (0-9)
            setSelectedGrade(value); // Convert to integer
        }
    };

    /**
     * @function handleSectionChange
     * @description Handles changes to the selected sections.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSectionChange = e => {
        setFilteredStudents({ students: [], meta: {}, header: {} });
        setSearchTerm("");
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSection([...selectedSection, value]);
        } else {
            setSelectedSection(selectedSection.filter((section) => section !== value));
        }
    };

    /**
     * @function handleSemesterChange
     * @description Handles changes to the selected semester.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSemesterChange = (e) => {
        setFilteredStudents({ students: [], meta: {}, header: {} });
        setSearchTerm("");
        setSelectedSemester(parseFloat(e.target.value));
    };

    /**
     * @function handleYearChange
     * @description Handles changes to the selected year.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleYearChange = e => setSelectedYear(e.target.value);

    /**
     * @function handleSearchChange
     * @description Handles changes to the search term.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSearchChange = (e) => {
        const value = e.target.value;
        setSearchTerm(value);           // Update the search term state
        if (value === "") {
            setFilteredStudents(allStudents);  // If search is cleared, revert to all students
        }
    };

    const handleSubjectChange = (e) => {
        setSelectedSubjectId(e.target.value);
        setSearchTerm("");
        if (e.target.value === "") {
            setGradeAssigned([]);
        } else {
            setFilteredStudents({ students: [], meta: {}, header: {} });
            fetchGrade();
        }
    };

    const fetchGrade = async () => {
        try {
            const response = await api.get('/teacher/students/assigned_grade');
            setGradeAssigned(response.data['grade']);
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                showAlert("warning", error.response.data['error']);
            } else {
                showAlert("warning", "An unexpected error occurred.");
            }
        }
    };


    /**
     * @hook useEffect
     * @description Fetches the assigned grades whenever the selected grade changes.
     * @returns {void}
     */
    useEffect(() => {
        /**
         * @description Fetches the subjects assigned to the teacher.
         */

        const subjectTaught = async () => {
            try {
                const response = await api.get('/teacher/assigned-subject');
                if (response.status === 200) {
                    setSubjectAssigned(response.data);
                }
            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    showAlert("warning", error.response.data['error']);
                } else {
                    showAlert("warning", "An unexpected error occurred.");
                }
            }
        };
        subjectTaught();
    }, []);

    return (
        <div className="dashboard-container">
            <div className="admin-header">
                <h2>Manage Students</h2>
            </div>
            <form onSubmit={(e) => handleSearch(e, 1)}>
                <section className="admin-filters">
                    <div className="filter-group">
                        <label htmlFor="Subject">Subject:</label>
                        <select
                            id="Subject"
                            value={selectedSubjectId}
                            onChange={handleSubjectChange}
                            required
                        >
                            <option value="">Select Subject</option>
                            {subjectAssigned &&
                                subjectAssigned.map((subject) =>
                                    <option key={subject.id} type="text" value={subject.id}>
                                        {subject.name}
                                    </option>
                                )}
                        </select>
                    </div>
                    <div className="filter-group">
                        <label htmlFor="grade">Grade:</label>
                        <select
                            id="grade"
                            value={selectedGrade}
                            onChange={handleGradeChange}
                            required
                        >
                            <option value="">Select Grade</option>
                            {(gradeAssigned && gradeAssigned.length > 0) &&
                                gradeAssigned.map(grade =>
                                    <option key={grade} value={grade}>
                                        grade {grade}
                                    </option>
                                )}
                        </select>
                    </div>
                    <div className="filter-group">
                        <label htmlFor="section">Section:</label>
                        <div className="checkbox-group stud-list">
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
                    <div className="filter-group">
                        <label htmlFor="semester">Semester:</label>
                        <select id="semester" value={selectedSemester} onChange={handleSemesterChange}>
                            {Array.from({ length: 2 }, (_, i) => i + 1).map(semester =>
                                <option key={semester} value={semester}>
                                    Semester {semester}
                                </option>
                            )}
                        </select>
                    </div>
                    <div className="filter-group">
                        <label htmlFor="year">Year:</label>
                        <select id="year" value={selectedYear} onChange={handleYearChange}>
                            {/* Dynamic Year Options */}
                            {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                                <option key={year} value={`${year}/${(year + 1) % 100}`}>
                                    {year}/{(year + 1) % 100}
                                </option>
                            ))}
                        </select>
                    </div>
                    <button className="filter-group-search" type="submit">
                        Search
                    </button>
                </section>
            </form>
            <Alert
                type={alert.type}
                message={alert.message}
                show={alert.show}
                onClose={closeAlert}
            />
            {/* Student List */}
            <StudentList
                searchTerm={searchTerm}
                handleSearchChange={handleSearchChange}
                handleSearch={handleSearch}
                filteredStudents={filteredStudents}
                toggleDropdown={toggleDropdown}
                studentSummary={studentSummary}
            />
            {filteredStudents.meta.total_pages > 1 &&
                <Pagination
                    handlePreviousPage={handlePreviousPage}
                    currentPage={currentPage}
                    handleNextPage={handleNextPage}
                    meta={filteredStudents.meta}
                />
            }
        </div>
    );
};

export default TeacherStudentsList;
