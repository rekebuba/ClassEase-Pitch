import React, { useState } from 'react';
import './styles/StudRegistrationForm.css';


const StudentRegistrationForm = () => {
  const [formData, setFormData] = useState({
    name: "",
    FatherName: "",
    GrandFatherName: "",
    grade: "",
    dob: "",
    FatherPhone: ""
  });

  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    console.log("Form Submitted:", formData);
  };

  return (
    <div className="registration-form-container">
      <h2>Student Registration Form</h2>
      <form onSubmit={handleSubmit} className="student-form">
        <div className="registration-form-group">
          <label htmlFor="firstName">Name:</label>
          <input
            type="text"
            id="firstName"
            name="firstName"
            value={formData.firstName}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="registration-form-group">
          <label htmlFor="lastName">Father Name:</label>
          <input
            type="text"
            id="lastName"
            name="lastName"
            value={formData.lastName}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="registration-form-group">
          <label htmlFor="lastName">Grand Father Name:</label>
          <input
            type="text"
            id="grandFatherName"
            name="grandFatherName"
            value={formData.grandFatherName}
            onChange={handleInputChange}
            required
          />
        </div>

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
            {Array.from({ length: 12 }, (_, i) => i + 1).map(grade =>
              <option key={grade} value={grade}>
                Grade {grade}
              </option>
            )}
          </select>
        </div>
        <div className="registration-form-group">
          <label htmlFor="dob">Date of Birth:</label>
          <input
            type="date"
            id="dob"
            name="dob"
            value={formData.dob}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="registration-form-group">
          <label htmlFor="phone">Phone Number:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            required
          />
        </div>

        <button type="submit" className="submit-btn">
          Register
        </button>
      </form>
    </div>
  );
};

export default StudentRegistrationForm;
