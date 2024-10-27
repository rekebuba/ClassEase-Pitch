import React, { useState } from 'react';
import '../../styles/StudRegistrationForm.css';
import Api from '../../services/api';
import Alert from "../../services/Alert";
import convertKeysToSnakeCase from '../library/lodash';

/**
 * StudentRegistrationForm component handles the registration form for students.
 * It manages form state, handles form submission, and displays alerts based on the response.
 *
 * @component
 * @example
 * return (
 *   <StudentRegistrationForm />
 * )
 *
 * @returns {JSX.Element} The rendered component.
 *
 * @typedef {Object} FormData
 * @property {string} name - The student's name.
 * @property {string} fatherName - The student's father's name.
 * @property {string} grandFatherName - The student's grandfather's name.
 * @property {string} grade - The student's grade.
 * @property {string} dateOfBirth - The student's date of birth.
 * @property {string} fatherPhone - The student's father's phone number.
 * @property {string} motherPhone - The student's mother's phone number.
 * @property {string} startYear - The year the student is registering for.
 */
const StudentRegistrationForm = () => {
  const [alert, setAlert] = useState({ type: "", message: "", show: false });
  const [currentYear] = useState(new Date().getFullYear());
  const [formData, setFormData] = useState({
    name: "",
    fatherName: "",
    grandFatherName: "",
    grade: "",
    dateOfBirth: "",
    fatherPhone: "",
    motherPhone: "",
    startYear: ""
  });

  /**
   * @function handleSubmit
   * @description Handles form submission, sends data to the server, and displays alerts based on the response.
   * @param {Event} e - The form submission event.
   * @async
   * @returns {Promise<void>} A promise that resolves when the form submission is complete.
   * @throws {Error} An error if the form submission fails.
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    const snakeCaseFormData = convertKeysToSnakeCase(formData);
    try {
      const response = await Api.post('/student/registration', snakeCaseFormData);
      showAlert("success", response.data['message']);
      // clear the form inputs (keeps user on same page)
      setFormData({
        name: "",
        fatherName: "",
        grandFatherName: "",
        grade: "",
        dateOfBirth: "",
        fatherPhone: "",
        motherPhone: "",
        startYear: ""
      });
    } catch (error) {
      if (error.response && error.response.data && error.response.data['error']) {
        showAlert("warning", error.response.data['error']);
      } else {
        showAlert("warning", "An unexpected error occurred.");
      }
    }
  };

  /**
   * @function handleInputChange
   * @description Handles input changes and updates the form state.
   * @param {Event} e - The input change
   * @returns {void}
   */
  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  /**
   * @function showAlert
   * @description Displays an alert with the specified type and message.
   * @param {string} type - The type of alert (e.g., "success", "warning").
   * @param {string} message - The alert message.
   * @returns {void}
   */
  const showAlert = (type, message) => {
    setAlert({ type, message, show: true });
  };

  /**
   * @function closeAlert
   * @description Closes the currently displayed alert.
   * @returns {void}
   */
  const closeAlert = () => {
    setAlert({ ...alert, show: false });
  };

  return (
    <div className="registration-form-container">
      <h2>Student Registration Form</h2>
      <form onSubmit={handleSubmit} className="student-form">
        <div className="name-section">
          <div className="registration-form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="registration-form-group">
            <label htmlFor="FatherName">Father Name:</label>
            <input
              type="text"
              id="fatherName"
              name="fatherName"
              value={formData.fatherName}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="registration-form-group">
            <label htmlFor="GrandFatherName">Grand Father Name:</label>
            <input
              type="text"
              id="grandFatherName"
              name="grandFatherName"
              value={formData.grandFatherName}
              onChange={handleInputChange}
              required
            />
          </div>
        </div>

        <div className="date-section">
          <div className="registration-form-group">
            <label htmlFor="grade">Grade:</label>
            <select
              id="grade"
              name="grade"
              value={formData.grade}
              onChange={handleInputChange}
              required
            >
              <option value="">Select Grade</option>
              {Array.from({ length: 12 }, (_, i) => i + 1).map(grade => (
                <option key={grade} value={grade}>
                  Grade {grade}
                </option>
              ))}
            </select>
          </div>

          <div className="registration-form-group">
            <label htmlFor="year">Register For The Year:</label>
            <select
              id="startYear"
              name="startYear"
              value={formData.startYear}
              onChange={handleInputChange}
              required
            >
              <option value="">Registration Year</option>
              {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                <option key={year} value={year}>
                  {year}/{(year + 1) % 100}
                </option>
              ))}
            </select>
          </div>
          <div className="registration-form-group">
            <label htmlFor="dateOfBirth">Date of Birth:</label>
            <input
              type="date"
              id="dateOfBirth"
              name="dateOfBirth"
              value={formData.dateOfBirth}
              onChange={handleInputChange}
              required
            />
          </div>
        </div>

        <div className="parent-section">
          <div className="registration-form-group">
            <label htmlFor="fatherPhone">Father Phone Number:</label>
            <input
              type="tel"
              id="fatherPhone"
              name="fatherPhone"
              value={formData.fatherPhone}
              onChange={handleInputChange}
            />
          </div>
          <div className="registration-form-group">
            <label htmlFor="motherPhone">Mother Phone Number:</label>
            <input
              type="tel"
              id="motherPhone"
              name="motherPhone"
              value={formData.motherPhone}
              onChange={handleInputChange}
            />
          </div>
          {alert.show && (
            <Alert
              type={alert.type}
              message={alert.message}
              show={alert.show}
              onClose={closeAlert}
            />
          )}
        </div>
        <button type="submit" className="submit-btn">
          Register
        </button>
      </form>
    </div>
  );
};

export default StudentRegistrationForm;
