
import React, { useState } from "react";
import { FaSearch } from 'react-icons/fa';
import DataExport from './DataExport'

const AdminTeachList = ({ toggleDropdown }) => {
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
                <h2>Manage Teachers</h2>
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
                    <h3>Teachers List</h3>
                    <DataExport />
                    <div className="search-bar">
                        <input
                            type="text"
                            placeholder="Search by Teacher ID"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <button onClick={handleSearch}>
                            <FaSearch />
                        </button>
                    </div>
                </div>

                <div className="data-section">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Subject</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>9876</td>
                                <td>Mr. Anderson</td>
                                <td>Mathematics</td>
                                <td>
                                    <button className="detail-btn" onClick={toggleDropdown}>Detail</button>
                                </td>
                            </tr>
                            <tr>
                                <td>5432</td>
                                <td>Ms. Thompson</td>
                                <td>English</td>
                                <td>
                                    <button className="detail-btn" onClick={toggleDropdown}>Detail</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>
        </div>
    );
};

export default AdminTeachList;
