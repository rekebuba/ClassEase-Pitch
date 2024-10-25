
import React, { useState, useEffect } from "react";
import { FaSearch } from 'react-icons/fa';
import Pagination from "./library/pagination";
import Alert from "./Alert";
import api from "../services/api";

const AdminTeachList = ({ toggleDropdown, teacherSummary }) => {
    const [alert, setAlert] = useState({ type: "", message: "", show: false });
    const [allTeacher, setAllStudents] = useState({ teachers: [], meta: {} });        // Store all teachers
    const [filteredTeachers, setFilteredTeachers] = useState({ teachers: [], meta: {} });  // Store the filtered search results
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const limit = 10;

    const handleSearch = async (page) => {
        page = page || currentPage; // If page is not provided, use the current page
        try {
            const response = await api.get('/admin/teachers', {
                params: {
                    page: page,
                    limit: limit,
                    search: searchTerm
                }
            });

            console.log(response.data);
            const data = {
                teachers: response.data['teachers'],
                meta: response.data['meta']
            };

            if (searchTerm) {
                setFilteredTeachers(data); // Update with search results
            } else {
                setAllStudents(data);      // Store all teachers
                setFilteredTeachers(data); // Initially, filtered is the same as all
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
            setFilteredTeachers({ teachers: [], meta: {} });
        }
    };

    useEffect(() => {
        handleSearch();  // Fetch the list of Teachers when the component loads
    }, []);


    const handleNextPage = () => {
        if (currentPage < filteredTeachers.meta.total_pages) {
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

    const handleSearchChange = (e) => {
        const value = e.target.value;
        setSearchTerm(value);           // Update the search term state
        if (value === "") {
            setFilteredTeachers(allTeacher);  // If search is cleared, revert to all teachers
        }
    };


    return (
        <div className="manage-student-container">
            <div className="admin-header">
                <h2>Manage Teachers</h2>
            </div>
            <section className="student-list">
                <div className="list-head">
                    <h3>Teachers List</h3>
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
                                <th>Last Name</th>
                                <th>Class Assigned</th>
                                <th>Subject</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        {filteredTeachers.teachers.map(teacher => <tbody>
                            {/* Dynamic Data Rows */}
                            <tr>
                                <td>{teacher.id}</td>
                                <td>Mr. {teacher.first_name}</td>
                                <td>{teacher.last_name}</td>
                                <td>{teacher.record.length > 0 ? teacher.record.length : 'N/A'}</td>
                                <td>{teacher.subjects}</td>
                                <td>
                                    <div className="action-container">
                                        <button className="detail-btn" onClick={() => {
                                            toggleDropdown('detail');
                                            teacherSummary(teacher); // Pass the data for the clicked Teacher
                                        }}>Detail</button>
                                        <button className="edit-btn" onClick={() => {
                                            toggleDropdown('edit');
                                            teacherSummary(teacher); // Pass the data for the clicked Teacher
                                        }}>Edit</button>
                                        <button className="delete-btn">Delete</button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>)}
                    </table>
                </div>
            </section>
            {filteredTeachers.meta.total_pages > 1 &&
                <Pagination
                    handlePreviousPage={handlePreviousPage}
                    currentPage={currentPage}
                    handleNextPage={handleNextPage}
                    meta={filteredTeachers.meta}
                />}
            <Alert
                type={alert.type}
                message={alert.message}
                show={alert.show}
                onClose={closeAlert}
            />
        </div>
    );
};

export default AdminTeachList;
