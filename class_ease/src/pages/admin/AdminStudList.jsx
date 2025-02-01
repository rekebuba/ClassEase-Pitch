import { useState } from "react";
import { FaSearch } from 'react-icons/fa';
import api from "../../services/api";
import Alert from "../../services/Alert";
import Pagination from "../library/pagination";
import '../../styles/Table.css';

/**
 * @function StudentList - Displays a list of students with search functionality.
 * @param {Object} props - The component props.
 * @param {string} props.searchTerm - The current search term for filtering students by name.
 * @param {Function} props.handleSearchChange - Function to handle changes in the search input.
 * @param {Function} props.handleSearch - Function to handle the search functionality.
 * @param {Object} props.filteredStudents - The state containing filtered students data.
 * @param {Function} props.toggleProfile - Function to toggle the profile view.
 * @param {Function} props.profileSummary - Function to display the profile summary for a student.
 * @returns {JSX.Element} The rendered StudentList component.
 * @description
 * This component displays a list of students with search functionality. It allows users to search
 * for students by name and view their details. The component includes a search input field, a search
 * button, and a table displaying the student data. Each row in the table contains the student's ID,
 * name, father's name, grandfather's name, section, and a button to view the student's details.
 */
function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, toggleProfile, profileSummary }) {
    return (
        <section className="table-section">
            {(filteredStudents.students.length > 0) && (
                <div className="table-head">
                    <h3>Student List</h3>
                    <h3>
                        <span>{`Academic Year: ${filteredStudents.header.year}`}</span>
                        <span style={{ marginLeft: '20px' }}>{`Grade: ${filteredStudents.header.grade}`}</span>
                    </h3>
                    <div className="table-search-bar">
                        <input
                            type="text"
                            placeholder="Search Student"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <button onClick={() => handleSearch()}>
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
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredStudents.students.map((student, index) => (
                        // Dynamic Data Rows
                        <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
                            <td>{student.student_id}</td>
                            <td>{student.name}</td>
                            <td>{student.father_name}</td>
                            <td>{student.grand_father_name}</td>
                            <td>{student.section ? student.section : 'N/A'}</td>
                            <td>
                                <button className="detail-btn" onClick={() => {
                                    toggleProfile();
                                    profileSummary(student); // Pass the data for the clicked student
                                }}>Detail</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </section>
    );
}


/**
 * AdminStudentsList component for managing and displaying a list of students.
 *
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.toggleProfile - Function to toggle the profile view.
 * @param {Object} props.profileSummary - Object containing profile summary data.
 *
 * @returns {JSX.Element} The rendered AdminStudentsList component.
 *
 * @example
 * <AdminStudentsList toggleProfile={toggleProfileFunction} profileSummary={profileSummaryData} />
 *
 * @description
 * This component allows administrators to manage and view a list of students. It includes
 * functionality for filtering students by grade and year, searching students by name, and
 * pagination to navigate through the list of students. The component also handles displaying
 * alerts for any errors that occur during the search process.
 *
 * @property {number} selectedGrade - The currently selected grade for filtering students.
 * @property {string} selectedYear - The currently selected year for filtering students.
 * @property {Object} alert - The alert state containing type, message, and visibility status.
 * @property {Object} allStudents - The state storing all students data.
 * @property {Object} filteredStudents - The state storing filtered students data based on search.
 * @property {string} searchTerm - The current search term for filtering students by name.
 * @property {number} currentPage - The current page number for pagination.
 * @property {number} currentYear - The current year.
 * @property {number} limit - The limit of students per page.
 */
const AdminStudentsList = ({ toggleProfile, profileSummary }) => {
    const [selectedGrade, setSelectedGrade] = useState(1);
    const [selectedYear, setSelectedYear] = useState("2024/25");
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [allStudents, setAllStudents] = useState({ students: [], meta: {} });        // Store all students
    const [filteredStudents, setFilteredStudents] = useState({ students: [], meta: {}, header: {} });  // Store the filtered search results
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [currentYear] = useState(new Date().getFullYear());
    const limit = 10;

    /**
     * @function handleSearch - Handles the search functionality and updates the state with search results.
     * @param {number} page - The page number for pagination.
     * @returns {Promise<void>} - A promise that resolves when the search is complete.
     * @description
     * This function makes an API request to search for students based on the selected grade, year, and search term.
     * It updates the state with the search results and handles pagination by setting the current page.
     * If an error occurs during the search, an alert is displayed with the error message.
     * The function also resets the current page and state if an error occurs.
     */
    const handleSearch = async (page) => {
        page = page || currentPage; // If page is not provided, use the current page
        try {
            const response = await api.get('/admin/manage/students', {
                params: {
                    grade: selectedGrade,
                    year: selectedYear,
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

    /**
     * @function handleNextPage - Handles the pagination to the next page.
     * @description
     * This function increments the current page number and calls the handleSearch function
     * to fetch the next page of students based on the current search criteria.
     * If the current page is less than the total number of pages, the search is performed.
     * Otherwise, the function does nothing.
     * The function is triggered when the user clicks on the next page button in the pagination component.
     * The function also updates the current page state.
     * @returns {void}
     */
    const handleNextPage = () => {
        if (currentPage < filteredStudents.meta.total_pages) {
            const newPage = currentPage + 1;  // Increment the page
            handleSearch(newPage);
        }
    };

    /**
     * @function handlePreviousPage - Handles the pagination to the previous page.
     * @description
     * This function decrements the current page number and calls the handleSearch function
     * to fetch the previous page of students based on the current search criteria.
     * If the current page is greater than 1, the search is performed.
     * Otherwise, the function does nothing.
     */
    const handlePreviousPage = () => {
        if (currentPage > 1) {
            const newPage = currentPage - 1;  // Decrement the page
            handleSearch(newPage);
        }
    };

    /**
     * @function showAlert - Displays an alert with a specified type and message.
     * @param {string} type - The type of alert (e.g., "success", "warning", "error").
     * @param {string} message - The message to display in the alert.
     * @returns {void}
     * @description
     * This function updates the alert state with the specified type and message
     * and sets the visibility status to true to display the alert.
     * The function is used to show feedback messages to the user based on the result of an action.
     */
    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    /**
     * @function closeAlert - Closes the currently displayed alert.
     * @returns {void}
     * @description
     * This function updates the alert state to hide the currently displayed alert
     * by setting the visibility status to false. The function is triggered
     * for a certain timeout period.
     */
    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    /**
     * @function handleGradeChange - Updates the selected grade state.
     * @param {Object} e - The event object representing the grade selection.
     * @returns {void}
     * @description
     * This function updates the selected grade state based on the value selected
     */
    const handleGradeChange = e => setSelectedGrade(parseFloat(e.target.value));

    /**
     * @function handleYearChange - Updates the selected year state.
     * @param {Object} e - The event object representing the year selection.
     * @returns {void}
     * @description
     * This function updates the selected year state based on the value selected
     * and triggers the handleSearch function to fetch students based on the new year.
     */
    const handleYearChange = e => {
        setSelectedYear(e.target.value);
    };

    /**
     * @function handleSearchChange - Updates the search term state and filters students accordingly.
     * @param {Object} e - The event object representing the search input.
     * @returns {void}
     * @description
     * This function updates the search term state based on the input value entered by the user.
     * If the search term is cleared, the filtered students are reverted to all students.
     */
    const handleSearchChange = (e) => {
        const value = e.target.value;
        setSearchTerm(value);           // Update the search term state
        if (value === "") {
            setFilteredStudents(allStudents);  // If search is cleared, revert to all students
        }
    };

    return (
        <div className="manage-student-container">
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
                        {Array.from({ length: 12 }, (_, i) => i + 1).map(grade =>
                            <option key={grade} value={grade}>
                                Grade {grade}
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
                toggleProfile={toggleProfile}
                profileSummary={profileSummary}
            />
            {
                (filteredStudents.meta.total_pages > 1 && filteredStudents.students.length >= limit) &&
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

export default AdminStudentsList;
