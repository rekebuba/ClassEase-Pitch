import { useEffect, useState } from "react";
import { adminApi } from "@/api";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { StudentTable } from "@/features/admin/tables";

/**
 * AdminStudentsList component for managing and displaying a list of students.
 *
 * @description
 * This component allows administrators to manage and view a list of students. It includes
 * functionality for filtering students by grade and year, searching students by name, and
 * pagination to navigate through the list of students. The component also handles displaying
 * alerts for any errors that occur during the search process.
 *
 * @property {number} selectedGrade - The currently selected grade for filtering students.
 * @property {string} selectedYear - The currently selected year for filtering students.
 * @property {Object} allStudents - The state storing all students data.
 * @property {number} currentYear - The current year.
 */
const AdminStudentList = () => {
  const [selectedGrade, setSelectedGrade] = useState(1);
  const [selectedYear, setSelectedYear] = useState("2024/25");
  const [allStudents, setAllStudents] = useState({ students: [], meta: {} }); // Store all students
  const [currentYear] = useState(new Date().getFullYear());

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
  const handleSearch = async (e) => {
    e?.preventDefault(); // Prevent default if event exists
    try {
      const response = await adminApi.getStudents({
        grade: [1, 2],
        year: selectedYear,
      });

      console.log("Response:", response.data);

      const data = {
        students: response.data["students"],
        meta: response.data["meta"],
        header: response.data["header"],
      };

      setAllStudents(data); // Store all students
    } catch (error) {
      if (
        error.response &&
        error.response.data &&
        error.response.data["error"]
      ) {
        toast.error(error.response.data["error"], {
          description:
            "Please try again later, if the problem persists, contact the administrator.",
          style: { color: "red" },
        });
      } else {
        toast.error("An unexpected error occurred.", {
          description:
            "Please try again later, if the problem persists, contact the administrator.",
          style: { color: "red" },
        });
      }
    }
  };

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await adminApi.getStudents();

        console.log("Response:", response.data);
      } catch (error) {
        console.log("Error fetching students:", error);
      }
    };
    fetchStudents();
  }, []); // Fetch students when grade or year changes

  /**
   * @function handleGradeChange
   * @description Handles changes to the selected grade.
   * @param {Event} e - The change event.
   * @returns {void}
   */
  const handleGradeChange = (value) => setSelectedGrade(value);

  /**
   * @function handleYearChange
   * @description Handles changes to the selected year.
   * @param {Event} e - The change event.
   * @returns {void}
   */
  const handleYearChange = (value) => setSelectedYear(value);

  return (
    <div className="bg-gray-100">
      <form onSubmit={(e) => handleSearch(e, 1, {})}>
        <section className="flex flex-wrap justify-between bg-white p-4 rounded shadow w-full mb-10">
          <div style={{ width: "9rem" }}>
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
          <div style={{ width: "9rem" }}>
            <Select onValueChange={handleYearChange} required>
              <SelectTrigger className="w-full p-2 border border-gray-300 rounded bg-gray-50">
                <SelectValue placeholder="Select Year" />
              </SelectTrigger>
              <SelectContent>
                {Array.from({ length: 3 }, (_, i) => currentYear - i).map(
                  (year) => (
                    <SelectItem
                      key={year}
                      value={`${year}/${(year + 1) % 100}`}
                    >
                      {year}/{(year + 1) % 100}
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
      {/* <StudentTable data={allStudents.students} /> */}
    </div>
  );
};

export default AdminStudentList;
