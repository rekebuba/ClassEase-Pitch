import { useState, useEffect, useCallback } from "react";
import { FaSearch } from 'react-icons/fa';
import { adminApi } from '@/api';
import { toast } from "sonner"
// import Pagination from "../../library/pagination";


/**
 * AdminTeachList Component
 * 
 * @component
 * @param {Object} props - The component props.
 * @param {Function} props.toggleDropdown - Function to toggle the dropdown menu.
 * @param {Function} props.teacherSummary - Function to display the teacher summary.
 * 
 * @description
 * This component renders a list of teachers with search and pagination functionality.
 * It allows the admin to manage teachers by viewing details or editing their information.
 * 
 * @returns {JSX.Element} The rendered component.
 * 
 * @example
 * <AdminTeachList toggleDropdown={toggleDropdown} teacherSummary={teacherSummary} />
 */
const AdminTeachList = ({ toggleDropdown, teacherSummary }) => {
    const [allTeacher, setAllStudents] = useState({ teachers: [], meta: {} });        // Store all teachers
    const [filteredTeachers, setFilteredTeachers] = useState({ teachers: [], meta: {} });  // Store the filtered search results
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const limit = 10;

    const handleSearch = useCallback(async (page) => {
        page = page || currentPage; // If page is not provided, use the current page
        try {
            const response = await adminApi.getTeachers({
                page: page,
                limit: limit,
                search: searchTerm
            });

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
            // Reset the state
            setCurrentPage(1);
            setFilteredTeachers({ teachers: [], meta: {} });
        }
    }, [currentPage, searchTerm]);

    useEffect(() => {
        handleSearch(1);  // Fetch the list of Teachers when the component loads
    }, [handleSearch]);


    /**
     * @function handleNextPage
     * @description Handles pagination to the next page.
     * @returns {void}
     */
    const handleNextPage = () => {
        if (currentPage < filteredTeachers.meta.total_pages) {
            const newPage = currentPage + 1;  // Increment the page
            handleSearch(newPage);
        }
    };

    /**
     * @function handlePreviousPage
     * @description Handles pagination to the previous page.
     * @returns {void}
     */
    const handlePreviousPage = () => {
        if (currentPage > 1) {
            const newPage = currentPage - 1;  // Decrement the page
            handleSearch(newPage);
        }
    };

    /**
     * @function handleSearchChange
     * @param {Object} e - The event object.
     * @description Updates the search term state and filters the teachers list.
     * @returns {void}
     */
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
            <section className="table-section">
                <div className="table-head">
                    <h3>Teachers List</h3>
                    <div className="table-search-bar">
                        <input
                            type="text"
                            placeholder="Search by Teacher ID"
                            value={searchTerm}
                            onChange={handleSearchChange}
                        />
                        <button onClick={() => { handleSearch(); }}>
                            <FaSearch />
                        </button>
                    </div>
                </div>

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
                    <tbody>
                        {filteredTeachers.teachers.map((teacher, index) => (
                            // Dynamic Data Rows
                            <tr key={index} style={{ backgroundColor: index % 2 === 0 ? '#fff' : '#f1f1f1' }}>
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
                                        {/* <button className="delete-btn">Delete</button> */}
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </section >
            {/* {
                filteredTeachers.meta.total_pages > 1 &&
                <Pagination
                    handlePreviousPage={handlePreviousPage}
                    currentPage={currentPage}
                    handleNextPage={handleNextPage}
                    meta={filteredTeachers.meta}
                />
            } */}
        </div >
    );
};

export default AdminTeachList;
