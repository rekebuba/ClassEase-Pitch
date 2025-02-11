import { useState, useEffect, useCallback } from "react";
import { FaSearch } from 'react-icons/fa';
import api from "../../services/api";
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


function StudentList({ searchTerm, handleSearchChange, handleSearch, filteredStudents, toggleDropdown, studentSummary, currentPage }) {
    return (
        <section className="table-section">
            {(filteredStudents && filteredStudents.students && filteredStudents.students.length > 0) && (
                <form onSubmit={handleSearch}>
                    <div className="flex justify-between items-center mb-4">
                        <h3>Student List</h3>
                        <h3 className="text-lg font-semibold">
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
                        <th>No.</th>
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
                                <td>{index + ((currentPage - 1) * 10) + 1}</td>
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
    const [selectedSubject, setSelectedSubject] = useState('');
    const [selectedSemester, setSelectedSemester] = useState(1);
    const [selectedYear, setSelectedYear] = useState("");
    const [allStudents, setAllStudents] = useState({ students: [], header: {} });        // Store all students
    const [filteredStudents, setFilteredStudents] = useState({ students: [], meta: {}, header: {} });  // Store the filtered search results
    const [selectedSection, setSelectedSection] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const [currentYear] = useState(new Date().getFullYear());
    const [assigned, setAssigned] = useState({});
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
        page = page || currentPage; // If page is not provided, use the current page
        try {
            const response = await api.get('/teacher/students/mark_list', {
                params: {
                    subject_code: assigned[selectedSubject]['subject_code'] || '',
                    grade: selectedGrade,
                    year: selectedYear,
                    sections: selectedSection,
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
    }, [currentPage, selectedGrade, selectedSection, selectedSemester, selectedYear, searchTerm]);

    useEffect(() => {
        if (saveStudent) {
            handleSearch(undefined, currentPage);
            toggleSave(false);
        }
    }, [currentPage, saveStudent, handleSearch, toggleSave]);

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
     * @function handleSectionChange
     * @description Handles changes to the selected sections.
     * @param {Event} e - The change event.
     * @returns {void}
     */
    const handleSectionChange = (section) => {
        setFilteredStudents({ students: [], meta: {}, header: {} });
        setSearchTerm("");

        setSelectedSection(section);
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
        setSelectedSubject(value);
        setSearchTerm("");
        setFilteredStudents({ students: [], meta: {}, header: {} });

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
                const response = await api.get('/teacher/assigned');
                if (response.status === 200) {
                    setAssigned(response.data);
                }
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
                                {assigned && Object.keys(assigned).length !== 0 &&
                                    Object.keys(assigned).map((subject) =>
                                        <SelectItem key={subject} type="text" value={subject}>
                                            {subject}
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
                                {assigned && assigned[selectedSubject] &&
                                    assigned[selectedSubject]['grades'].map((grade) => (
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
                                {assigned && assigned[selectedSubject] &&
                                    assigned[selectedSubject]['sections'].map((section) => (
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
            {/* Student List */}
            <StudentList
                searchTerm={searchTerm}
                handleSearchChange={handleSearchChange}
                handleSearch={handleSearch}
                filteredStudents={filteredStudents}
                toggleDropdown={toggleDropdown}
                studentSummary={studentSummary}
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
