import { useState } from "react";
import { FaSearch } from 'react-icons/fa';
import api from "../../services/api";
import '../../styles/Table.css';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import {
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from "@/components/ui/pagination"
import { toast } from "sonner"

/**
 * @function StudentList - Displays a list of students with search functionality.
 * @param {Object} props - The component props.
 * @param {string} props.searchTerm - The current search term for filtering students by name.
 * @param {Function} props.handleSearchChange - Function to handle changes in the search input.
 * @param {Function} props.handleSearch - Function to handle the search functionality.
 * @param {Function} props.toggleProfile - Function to toggle the profile view.
 * @param {Object} props.filteredStudents - The state containing filtered students data.
 * @param {Function} props.profileSummary - Function to display the profile summary for a student.
 * @returns {JSX.Element} The rendered StudentList component.
 * @description
 * This component displays a list of students with search functionality. It allows users to search
 * for students by name and view their details. The component includes a search input field, a search
 * button, and a table displaying the student data. Each row in the table contains the student's ID,
 * name, father's name, grandfather's name, section, and a button to view the student's details.
 */
function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, toggleProfile, profileSummary, currentPage }) {
    return (
        <section className="table-section">
            {(filteredStudents.students.length > 0) && (
                <form onSubmit={handleSearch}>
                    <div className="flex justify-between items-center mb-4">
                        <h3>Student List</h3>
                        <h3 className="text-lg font-semibold">
                            <span>{`Academic Year: ${filteredStudents.header.year}`}</span>
                            <span className="ml-5">{`Grade: ${filteredStudents.header.grade}`}</span>
                        </h3>
                        <div className="flex items-center justify-between mr-4 w-100">
                            <Input
                                className="bg-white mr-3"
                                placeholder="Search Student"
                                value={searchTerm}
                                onChange={handleSearchChange}
                                required
                            />
                            <Button className="h-9 w-9"><FaSearch /></Button>
                        </div>
                    </div>
                </form>
            )}

            <table className="data-table">
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Father Name</th>
                        <th>G.Father Name</th>
                        <th>Section</th>
                        <th>AVR Score</th>
                        <th>Rank</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredStudents.students.map((student, index) => (
                        // Dynamic Data Rows
                        <tr key={index}
                            className={`bg-${index % 2 === 0 ? 'white' : 'gray-100'} hover:bg-gray-200`}>
                            <td>{index + ((currentPage - 1) * 10) + 1}</td>
                            <td>{student.student_id}</td>
                            <td>{student.name}</td>
                            <td>{student.father_name}</td>
                            <td>{student.grand_father_name}</td>
                            <td>{student.section ? student.section : 'N/A'}</td>
                            <td>{student.final_score ? student.final_score : '-' }</td>
                            <td>{student.rank ? student.rank : '-' }</td>
                            <td>
                                <Button className="h-9 w-15 hover:border-gray-50"
                                    onClick={() => {
                                        toggleProfile();
                                        profileSummary(student); // Pass the data for the clicked student
                                    }}>
                                    Detail
                                </Button>

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
    const handleSearch = async (e, page) => {
        e?.preventDefault(); // Prevent default if event exists
        setFilteredStudents({ students: [], meta: {}, header: {} }); // clear any search result for the new one
        setSearchTerm("");
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
            setFilteredStudents({ students: [], meta: {}, header: {} });
        }
    };

    const handlePageChange = (e, page) => {
        if (page > 0 && page <= filteredStudents.meta.total_pages) {
            handleSearch(e, page);
        }
    };

    /**
     * @function handleGradeChange
     * @description Handles changes to the selected grade.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleGradeChange = (value) => {
        setFilteredStudents({ students: [], meta: {}, header: {} }); // clear any search result for the new one
        setSearchTerm("");
        setSelectedGrade(value);
    };

    /**
     * @function handleYearChange
     * @description Handles changes to the selected year.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleYearChange = (value) => setSelectedYear(value);


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
        <div className="flex flex-col p-6 bg-gray-100">
            <form onSubmit={(e) => handleSearch(e, 1)}>
                <section className="flex flex-wrap justify-between bg-white p-4 rounded shadow w-full mb-10">
                    <div style={{ width: '9rem' }}>
                        <Select onValueChange={handleGradeChange} required>
                            <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                                <SelectValue placeholder="Select Grade" />
                            </SelectTrigger>
                            <SelectContent>
                                {Array.from({ length: 12 }, (_, i) => i + 1).map((grade) => (
                                    <SelectItem key={grade} value={`${grade}`}>
                                        Grade {grade}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div style={{ width: '9rem' }}>
                        <Select onValueChange={handleYearChange} required>
                            <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                                <SelectValue placeholder="Select Year" />
                            </SelectTrigger>
                            <SelectContent>
                                {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                                    <SelectItem key={year} value={`${year}/${(year + 1) % 100}`}>
                                        {year}/{(year + 1) % 100}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <Button>
                        Search
                    </Button>
                </section>
            </form>
            {/* Student List */}
            <StudentList
                searchTerm={searchTerm}
                handleSearchChange={handleSearchChange}
                handleSearch={handleSearch}
                filteredStudents={filteredStudents}
                toggleProfile={toggleProfile}
                profileSummary={profileSummary}
                currentPage={currentPage}
            />
            {filteredStudents.meta.total_pages > 1 && (
                <>
                    {/* Pagination Component */}
                    <Pagination className="mt-4">
                        <PaginationContent>
                            <PaginationItem>
                                <PaginationPrevious
                                    className="hover:bg-gray-200 hover:cursor-pointer"
                                    onClick={(e) => {
                                        handlePageChange(e, currentPage - 1);
                                    }}
                                />
                            </PaginationItem>

                            {[...Array(filteredStudents.meta.total_pages)].map((_, index) => (
                                <PaginationItem key={index}>
                                    <PaginationLink
                                        className="hover:bg-gray-200 hover:cursor-pointer"
                                        isActive={currentPage === index + 1}
                                        onClick={(e) => {
                                            handlePageChange(e, index + 1);
                                        }}
                                    >
                                        {index + 1}
                                    </PaginationLink>
                                </PaginationItem>
                            ))}

                            {filteredStudents.meta.total_pages > 5 &&
                                <PaginationItem>
                                    <PaginationEllipsis />
                                </PaginationItem>}

                            <PaginationItem>
                                <PaginationNext
                                    className="hover:bg-gray-200 hover:cursor-pointer"
                                    onClick={(e) => {
                                        handlePageChange(e, currentPage + 1);
                                    }}
                                />
                            </PaginationItem>
                        </PaginationContent>
                    </Pagination>
                </>
            )}
        </div>
    );
};

export default AdminStudentsList;
