import { useState, useEffect, useCallback } from "react";
import { FaSearch } from 'react-icons/fa';
// import Pagination from '../library/pagination';
import api from "../../services/api";
import Alert from '../../services/Alert';
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

function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, toggleDropdown, studentSummary }) {
    return (
        <section className="table-section">
            {(filteredStudents && filteredStudents.students && filteredStudents.students.length > 0) && (
                <form onSubmit={handleSearch}>
                    <div className="flex justify-between items-center mb-4 ">
                        <h3>Student List</h3>
                        <h3>
                            <span>{`Academic Year: ${filteredStudents.header.year}`}</span>
                            <span className="ml-5">{`Grade: ${filteredStudents.header.grade}`}</span>
                            <span className="ml-5">{`Subject: ${filteredStudents.header.subject}`}</span>
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
                            <tr key={index}
                                className={`bg-${index % 2 === 0 ? 'white' : 'gray-100'} hover:bg-gray-200`}>
                                <td>{student.student_id}</td>
                                <td>{student.name}</td>
                                <td>{student.father_name}</td>
                                <td>{student.grand_father_name}</td>
                                <td>{student.section ? student.section : 'N/A'}</td>
                                <td>{student.total_score ? student.total_score : 0}</td>
                                <td>{student.rank ? student.rank : 0}</td>
                                <td>
                                    <Button className="h-9 w-15 hover:border-gray-50"
                                        onClick={() => {
                                            toggleDropdown();
                                            studentSummary(student); // Pass the data for the clicked student
                                        }}>
                                        Detail
                                    </Button>
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
const TeacherStudentsList = ({ toggleDropdown, studentSummary, saveStudent, toggleSave }) => {
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
    const handleSearch = useCallback(async (e, page) => {
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
    }, [currentPage, selectedGrade, selectedSection, selectedSemester, selectedSubjectId, selectedYear, searchTerm]);

    // if (saveStudent) {
    //     console.log("filteredStudents", saveStudent);
    //     handleSearch(undefined, currentPage);
    //     toggleSave(false);
    // }
    // if (saveStudent) {
    //     handleSearch(undefined, currentPage);
    // }


    useEffect(() => {
        if (saveStudent) {
            handleSearch(undefined, currentPage);
            toggleSave(false);
        }
    }, [currentPage, saveStudent, handleSearch, toggleSave]);

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
    const handleGradeChange = (value) => {
        setFilteredStudents({ students: [], meta: {}, header: {} }); // clear any search result for the new one
        setSearchTerm("");
        console.log((value));
        setSelectedGrade(value); // Convert to integer
    };

    /**
     * @function handleSectionChange
     * @description Handles changes to the selected sections.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSectionChange = (section) => {
        setFilteredStudents({ students: [], meta: {}, header: {} });
        setSearchTerm("");

        setSelectedSection((prev) =>
            prev.includes(section) ? prev.filter((s) => s !== section) : [...prev, section]
        );
    };

    /**
     * @function handleSemesterChange
     * @description Handles changes to the selected semester.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSemesterChange = (value) => {
        setFilteredStudents({ students: [], meta: {}, header: {} });
        setSearchTerm("");
        setSelectedSemester(parseFloat(value));
    };

    /**
     * @function handleYearChange
     * @description Handles changes to the selected year.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleYearChange = (value) => setSelectedYear(value);

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

    const handleSubjectChange = (value) => {
        setSelectedSubjectId(value);
        setSearchTerm("");
        if (value === "") {
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

    const handlePageChange = (e, page) => {
        if (page > 0 && page <= filteredStudents.meta.total_pages) {
            handleSearch(e, page);
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
        <div className="flex flex-col p-6 bg-gray-100">
            <form onSubmit={(e) => handleSearch(e, 1)}>
                <section className="flex flex-wrap justify-between bg-white p-4 rounded shadow w-full mb-10">
                    <div style={{ width: '9rem' }}>
                        <Select onValueChange={handleSubjectChange} required>
                            <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                                <SelectValue placeholder="Select Subject" />
                            </SelectTrigger>
                            <SelectContent>
                                {subjectAssigned &&
                                    subjectAssigned.map((subject) =>
                                        <SelectItem key={subject.id} type="text" value={subject.id}>
                                            {subject.name}
                                        </SelectItem>
                                    )}
                            </SelectContent>
                        </Select>
                    </div>
                    <div style={{ width: '9rem' }}>
                        <Select onValueChange={handleGradeChange} required>
                            <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                                <SelectValue placeholder="Select Grade" />
                            </SelectTrigger>
                            <SelectContent>
                                {(gradeAssigned && gradeAssigned.length > 0) &&
                                    gradeAssigned.map((grade) => (
                                        <SelectItem key={grade} value={`${grade}`}>
                                            Grade {grade}
                                        </SelectItem>
                                    ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div style={{ width: '9rem' }}>
                        <Select onValueChange={handleSectionChange} required>
                            <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                                <SelectValue placeholder="Select Section" />
                            </SelectTrigger>
                            <SelectContent>
                                {['A', 'B', 'C'].map((section) => (
                                    <SelectItem key={section} value={section}>
                                        Section {section}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div style={{ width: '9rem' }}>
                        <Select onValueChange={handleSemesterChange} required>
                            <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                                <SelectValue placeholder="Select Semester" />
                            </SelectTrigger>
                            <SelectContent>
                                {Array.from({ length: 2 }, (_, i) => i + 1).map(semester =>
                                    <SelectItem key={semester} value={`${semester}`}>
                                        Semester {semester}
                                    </SelectItem>
                                )}
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

                            {filteredStudents.meta.total_pages > 5 && <PaginationItem><PaginationEllipsis /></PaginationItem>}

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

export default TeacherStudentsList;
