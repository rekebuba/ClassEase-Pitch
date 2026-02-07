import { useEffect, useState } from "react";
import { toast } from "sonner";

import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DataTable } from "@/features/teacher/tables";

import { studentColumn } from "./tables/studentColumns";

/**
 * TeacherStudentsList component for managing and displaying a list of students.
 *
 * @component
 * @param {object} props - The component props.
 * @param {Function} props.toggleDropdown - Function to toggle dropdown visibility.
 * @param {object} props.studentSummary - Summary information about students.
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @example
 * <TeacherStudentsList toggleDropdown={toggleDropdown} studentSummary={studentSummary} />
 *
 * @description
 * This component allows teachers to manage and filter a list of students based on various criteria such as grade, section, semester, and year. It also provides search functionality and pagination for navigating through the list of students.
 */
function TeacherStudentList() {
  const [selectedGrade, setSelectedGrade] = useState("");
  const [selectedSubject, setSelectedSubject] = useState("");
  const [selectedSemester, setSelectedSemester] = useState(1);
  const [selectedYear, setSelectedYear] = useState("");
  const [allStudents, setAllStudents] = useState({ students: [], header: {} }); // Store all students
  const [currentYear] = useState(new Date().getFullYear());
  const [assigned, setAssigned] = useState({});

  /**
   * @function handleSearch
   * @description Fetches and filters the list of students based on the selected criteria and search term.
   * @param {number} [page] - The page number to fetch. If not provided, the current page is used.
   * @returns {void}
   */
  const handleSearch = async (e) => {
    e?.preventDefault(); // Prevent default if event exists
    try {
      const response = await teacherApi.getStudents({
        subject_code: assigned[selectedSubject].subject_code || "",
        grade: selectedGrade,
        year: selectedYear,
        semester: selectedSemester,
      });

      const data = {
        students: response.data.students,
        meta: response.data.meta,
        header: response.data.header,
      };

      setAllStudents(data); // Store all students
    }
    catch (error) {
      if (
        error.response
        && error.response.data
        && error.response.data.error
      ) {
        toast.error(error.response.data.error, {
          description:
            "Please try again later, if the problem persists, contact the administrator.",
          style: { color: "red" },
        });
      }
      else {
        toast.error("An unexpected error occurred.", {
          description:
            "Please try again later, if the problem persists, contact the administrator.",
          style: { color: "red" },
        });
      }
    }
  };

  /**
   * @function handleGradeChange
   * @description Handles changes to the selected grade.
   * @param {Event} e - The change event.
   * @returns {void}
   */
  const handleGradeChange = value => setSelectedGrade(value);

  /**
   * @function handleSemesterChange
   * @description Handles changes to the selected semester.
   * @param {Event} e - The change event.
   * @returns {void}
   */
  const handleSemesterChange = value =>
    setSelectedSemester(Number.parseFloat(value));

  /**
   * @function handleYearChange
   * @description Handles changes to the selected year.
   * @param {Event} e - The change event.
   * @returns {void}
   */
  const handleYearChange = value => setSelectedYear(value);

  const handleSubjectChange = value => setSelectedSubject(value);

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
        const response = await teacherApi.getAssignedStudents();
        if (response.status === 200) {
          setAssigned(response.data);
        }
      }
      catch (error) {
        if (
          error.response
          && error.response.data
          && error.response.data.error
        ) {
          toast.error(error.response.data.error, {
            description:
              "Please try again later, if the problem persists, contact the administrator.",
            style: { color: "red" },
          });
        }
        else {
          toast.error("An unexpected error occurred.", {
            description:
              "Please try again later, if the problem persists, contact the administrator.",
            style: { color: "red" },
          });
        }
      }
    };
    subjectTaught();
  }, []);

  return (
    <div className="flex flex-col p-6 bg-gray-100">
      <form onSubmit={e => handleSearch(e)}>
        <section className="flex flex-wrap justify-between bg-white p-4 rounded shadow w-full mb-10">
          <div style={{ width: "9rem" }}>
            <Select onValueChange={handleSubjectChange} required>
              <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                <SelectValue placeholder="Select Subject" />
              </SelectTrigger>
              <SelectContent>
                {assigned
                  && Object.keys(assigned).length !== 0
                  && Object.keys(assigned).map(subject => (
                    <SelectItem key={subject} type="text" value={subject}>
                      {subject}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </div>
          <div style={{ width: "9rem" }}>
            <Select onValueChange={handleGradeChange} required>
              <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                <SelectValue placeholder="Select Grade" />
              </SelectTrigger>
              <SelectContent>
                {assigned
                  && assigned[selectedSubject]
                  && assigned[selectedSubject].grades.map(grade => (
                    <SelectItem key={grade} value={`${grade}`}>
                      Grade
                      {" "}
                      {grade}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </div>
          <div style={{ width: "9rem" }}>
            <Select onValueChange={handleSemesterChange} required>
              <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                <SelectValue placeholder="Select Semester" />
              </SelectTrigger>
              <SelectContent>
                {Array.from({ length: 2 }, (_, i) => i + 1).map(semester => (
                  <SelectItem key={semester} value={`${semester}`}>
                    Semester
                    {" "}
                    {semester}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div style={{ width: "9rem" }}>
            <Select onValueChange={handleYearChange} required>
              <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                <SelectValue placeholder="Select Year" />
              </SelectTrigger>
              <SelectContent>
                {Array.from({ length: 3 }, (_, i) => currentYear - i).map(
                  year => (
                    <SelectItem
                      key={year}
                      value={`${year}/${(year + 1) % 100}`}
                    >
                      {year}
                      /
                      {(year + 1) % 100}
                    </SelectItem>
                  ),
                )}
              </SelectContent>
            </Select>
          </div>
          <Button>Search</Button>
        </section>
      </form>
      {/* Student List */}
      <DataTable
        columns={studentColumn(handleSearch)}
        data={allStudents.students}
      />
    </div>
  );
}

export default TeacherStudentList;
