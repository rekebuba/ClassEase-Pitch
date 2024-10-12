import React, { useState } from "react";
import "./styles/AdminManageStudents.css";
import { FaSearch } from 'react-icons/fa';
import TeacherPanel from "../components/TeachPanel";


const TeacherManageStudents = () => {
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
        <div className="admin-manage-container">
            <TeacherPanel />
            <main className="admin-content">
                <header className="admin-header">
                    <h2>Manage Students</h2>
                </header>
                <section className="admin-filters">
                    <div className="filter-group">
                        <label htmlFor="grade">Grade:</label>
                        <select
                            id="grade"
                            value={selectedGrade}
                            onChange={handleGradeChange}
                        >
                            <option>All Grades</option>
                            <option>Grade 1</option>
                            <option>Grade 2</option>
                            <option>Grade 3</option>
                            <option>Grade 4</option>
                            <option>Grade 5</option>
                            <option>Grade 6</option>
                            <option>Grade 7</option>
                            <option>Grade 8</option>
                            <option>Grade 9</option>
                            <option>Grade 10</option>
                            <option>Grade 11</option>
                            <option>Grade 12</option>
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
                </section>

                <div className="list-head">
                    <h3>Student List</h3>
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
                <section className="student-list">
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
                                    <button className="edit-btn">Edit</button>
                                </td>
                            </tr>
                            <tr>
                                <td>5678</td>
                                <td>Jane Smith</td>
                                <td>Grade 11</td>
                                <td>B</td>
                                <td>2024</td>
                                <td>
                                    <button className="edit-btn">Edit</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </section>
            </main>
        </div>
    );
};

export default TeacherManageStudents;
