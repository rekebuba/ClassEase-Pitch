
import React, { useState } from "react";
import { FaSearch } from 'react-icons/fa';
import DataExport from "./DataExport";


const AdminStudentsList = ({ toggleDropdown }) => {
    const [selectedGrade, setSelectedGrade] = useState("All Grades");
    const [selectedSection, setSelectedSection] = useState("All Sections");
    const [selectedYear, setSelectedYear] = useState("2024");
    const [searchTerm, setSearchTerm] = useState("");

    const handleSearch = () => {
        // Add search logic here
    };

    const handleGradeChange = e => setSelectedGrade(e.target.value);
    const handleSectionChange = e => setSelectedSection(e.target.value);
    const handleYearChange = e => setSelectedYear(e.target.value);
    const handleSearchChange = e => setSearchTerm(e.target.value);

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
                    <label htmlFor="section">Section:</label>
                    <select
                        id="section"
                        value={selectedSection}
                        onChange={handleSectionChange}
                    >
                        <option>All Sections</option>
                        <option>A</option>
                        <option>B</option>
                        <option>C</option>
                    </select>
                </div>
                <div className="filter-group">
                    <label htmlFor="year">Year:</label>
                    <select id="year" value={selectedYear} onChange={handleYearChange}>
                        <option>2023</option>
                        <option>2024</option>
                        <option>2025</option>
                    </select>
                </div>
                <button className="filter-group-search" onClick={handleSearch}>
                    Search
                </button>
            </section>

            <section className="student-list">
                <div className="list-head">
                    <h3>Student List:</h3>
                    <DataExport />
                    <div className="search-bar">
                        <input
                            type="text"
                            placeholder="Search by Student ID"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <button onClick={handleSearch}>
                            <FaSearch />
                        </button>
                    </div>
                </div>

                <table className="data-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Grade</th>
                            <th>Section</th>
                            <th>Year</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {/* Dynamic Data Rows */}
                        <tr>
                            <td>1234</td>
                            <td>John Doe</td>
                            <td>Grade 10</td>
                            <td>A</td>
                            <td>2024</td>
                            <td>
                                <button className="detail-btn" onClick={toggleDropdown}>Detail</button>
                                {/* <button className="edit-btn">Edit</button> */}
                                {/* <button className="delete-btn">Delete</button> */}
                            </td>
                        </tr>
                        <tr>
                            <td>5678</td>
                            <td>Jane Smith</td>
                            <td>Grade 11</td>
                            <td>B</td>
                            <td>2024</td>
                            <td>
                                <button className="detail-btn" onClick={toggleDropdown}>Detail</button>
                                {/* <button className="edit-btn">Edit</button>
                  <button className="delete-btn">Delete</button> */}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </section>
        </div>
    );
};

export default AdminStudentsList;
