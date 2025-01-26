import { useState, useEffect } from "react";
import { FaSearch } from 'react-icons/fa';
import Pagination from '../library/pagination';
import api from "../../services/api";
import Alert from '../../services/Alert';

function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, currentStudents, toggleDropdown, studentSummary }) {
    return (
        <section className="table-section">
            {(filteredStudents && filteredStudents.students && filteredStudents.students.length > 0) && (
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
                        />
                        <button onClick={() => {
                            console.log('filteredStudents', filteredStudents);
                            handleSearch();
                            }}>
                            <FaSearch />
                        </button>
                    </div>
                </div>
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
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {(currentStudents && currentStudents.students) &&
                        currentStudents.students.map((student, index) => (
                            // Dynamic Data Rows
                            <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                                <td>{student.student_id}</td>
                                <td>{student.name}</td>
                                <td>{student.father_name}</td>
                                <td>{student.grand_father_name}</td>
                                <td>{student.section ? student.section : 'N/A'}</td>
                                <td>{student.total_score ? student.total_score : 0}</td>
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
    const [selectedGrade, setSelectedGrade] = useState(1);
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [selectedYear, setSelectedYear] = useState("2024/25");
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [allStudents, setAllStudents] = useState({ students: [], header: {} });        // Store all students
    const [filteredStudents, setFilteredStudents] = useState({ students: [], header: {} });  // Store the filtered search results
    const [selectedSection, setSelectedSection] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [currentYear] = useState(new Date().getFullYear());
    const [gradeAssigned, setGradeAssigned] = useState([]);
    const [currentStudents, setCurrentStudents] = useState({ students: [], header: {} });
    const [totalPages, setTotalPages] = useState(0);
    const limit = 10;

    /**
     * @function handleSearch
     * @description Fetches and filters the list of students based on the selected criteria and search term.
     * @param {number} [page] - The page number to fetch. If not provided, the current page is used.
     * @returns {void}
     */
    const handleSearch = async (page) => {
        if (selectedSection.length === 0) {
            showAlert("warning", "Select Section");
            return;
        }
        page = page || currentPage; // If page is not provided, use the current page
        try {
            const response = await api.get('/teacher/students/mark_list', {
                params: {
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
            setFilteredStudents({ students: [], header: {} });
        }
    };


    useEffect(() => {
        if (Object.keys(saveStudent).length === 0) {
            return;
        }
        const found = currentStudents.students.find(items => items.student_id === saveStudent.student_id);
        found.total_score = saveStudent.score;
    }, [saveStudent, currentStudents.students]);

    // Handle Next Page
    const handleNextPage = () => {
        if (currentPage < totalPages) {
            setCurrentPage((prevPage) => prevPage + 1);
        }
    };

    // Handle Previous Page
    const handlePreviousPage = () => {
        if (currentPage > 1) {
            setCurrentPage((prevPage) => prevPage - 1);
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
    const handleGradeChange = e => setSelectedGrade(parseFloat(e.target.value));

    /**
     * @function handleSectionChange
     * @description Handles changes to the selected sections.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSectionChange = e => {
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

    /**
     * @hook useEffect
     * @description Fetches the assigned grades whenever the selected grade changes.
     * @returns {void}
     */
    useEffect(() => {
        /**
         * @description Fetches the grades assigned to the teacher.
         */
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

            // Calculate the start and end indices for the students on the current page

            if (filteredStudents && filteredStudents.students) {
                const indexOfLastStudent = currentPage * limit;
                const indexOfFirstStudent = indexOfLastStudent - limit;
                setCurrentStudents({
                    students: filteredStudents.students.slice(indexOfFirstStudent, indexOfLastStudent),
                    header: filteredStudents.header
                });
                // Calculate total pages
                setTotalPages(Math.ceil(filteredStudents.students.length / limit));
            }
        };
        fetchGrade();
    }, [selectedGrade, currentPage, filteredStudents]);

    return (
        <div className="dashboard-container">
            <div className="admin-header">
                <h2>Manage Students</h2>
            </div>
            <section className="admin-filters">
                <div className="filter-group">
                    <label htmlFor="grade">Grade:</label>
                    <select
                        id="grade"
                        value={selectedGrade}
                        onChange={handleGradeChange}
                    >
                        {(gradeAssigned && gradeAssigned.length > 0) &&
                            gradeAssigned.map(grade =>
                                <option key={grade} type="text" defaultValue={grade}>
                                    Grade {grade}
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
                <button className="filter-group-search"
                    onClick={() => {
                        setSearchTerm(""); // Clear the search term
                        handleSearch();
                    }}>
                    Search
                </button>
            </section>
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
                currentStudents={currentStudents}
                toggleDropdown={toggleDropdown}
                studentSummary={studentSummary}
            />
            {
                (totalPages > 1 && filteredStudents && filteredStudents.students && filteredStudents.students.length >= limit) &&
                <Pagination
                    handlePreviousPage={handlePreviousPage}
                    currentPage={currentPage}
                    handleNextPage={handleNextPage}
                    meta={{
                        total_pages: totalPages
                    }}
                />
            }
        </div>
    );
};

export default TeacherStudentsList;
