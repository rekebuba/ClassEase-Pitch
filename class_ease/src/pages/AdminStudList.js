import React, { useState } from "react";
import { FaSearch } from 'react-icons/fa';
import api from "../services/api";
import Alert from "./Alert"
import Pagination from "./library/pagination";


function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, toggleDropdown, studentSummary }) {
    return (
        <section className="student-list">
            <div className="list-head">
                <h3>Student List:</h3>
                <div className="search-bar">
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

            <table className="data-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Father Name</th>
                        <th>Grade</th>
                        <th>Section</th>
                        <th>Year</th>
                        <th>Action</th>
                    </tr>
                </thead>
                {filteredStudents.students.map(student => <tbody>
                    {/* Dynamic Data Rows */}
                    <tr>
                        <td>{student.student_id}</td>
                        <td>{student.name}</td>
                        <td>{student.father_name}</td>
                        <td>{student.grade}</td>
                        <td>{student.section ? student.section : 'N/A'}</td>
                        <td>{student.year}</td>
                        <td>
                            <button className="detail-btn" onClick={() => {
                                toggleDropdown();
                                studentSummary(student); // Pass the data for the clicked student
                            }}>Detail</button>
                        </td>
                    </tr>
                </tbody>)}
            </table>
        </section>
    );
}


const AdminStudentsList = ({ toggleDropdown, studentSummary }) => {
    const [selectedGrade, setSelectedGrade] = useState(1);
    const [selectedYear, setSelectedYear] = useState("2024/25");
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [allStudents, setAllStudents] = useState({ students: [], meta: {} });        // Store all students
    const [filteredStudents, setFilteredStudents] = useState({ students: [], meta: {} });  // Store the filtered search results
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [currentYear] = useState(new Date().getFullYear());
    const limit = 10;


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
                meta: response.data['meta']
            };

            console.log(searchTerm)
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
            setFilteredStudents({ students: [], meta: {} });
        }
    };

    const handleNextPage = () => {
        if (currentPage < filteredStudents.meta.total_pages) {
            const newPage = currentPage + 1;  // Increment the page
            handleSearch(newPage);
        }
    };

    const handlePreviousPage = () => {
        if (currentPage > 1) {
            const newPage = currentPage - 1;  // Decrement the page
            handleSearch(newPage);
        }
    };

    const showAlert = (type, message) => {
        setAlert({ type, message, show: true });
    };

    const closeAlert = () => {
        setAlert({ ...alert, show: false });
    };

    const handleGradeChange = e => setSelectedGrade(parseFloat(e.target.value));
    // const handleSectionChange = e => {
    //     const { value, checked } = e.target;
    //     if (checked) {
    //         setSelectedSection([...selectedSection, value]);
    //     } else {
    //         setSelectedSection(selectedSection.filter((section) => section !== value))
    //     }
    // }
    const handleYearChange = e => setSelectedYear(e.target.value);

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
                {/* <div className="filter-group">
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
                </div> */}
                <div className="filter-group">
                    <label htmlFor="year">Year:</label>
                    <select id="year" value={selectedYear} onChange={handleYearChange}>
                        {/* Dynamic Year Options */}
                        {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                            <option key={year} value={year}>
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
                toggleDropdown={toggleDropdown}
                studentSummary={studentSummary}
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
