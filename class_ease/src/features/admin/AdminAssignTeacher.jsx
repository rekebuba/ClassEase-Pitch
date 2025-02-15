import { useState, useEffect } from 'react';
import { FaTimes } from 'react-icons/fa';
import { toast } from "sonner"
import { adminApi } from '@/api';


/**
 * AdminAssignTeacher component allows an admin to assign a teacher to classes.
 *
 * @component
 * @param {Object} props - The properties object.
 * @param {boolean} props.isEditOpen - Indicates if the edit profile popup is open.
 * @param {Function} props.toggleEditProfile - Function to toggle the edit profile popup.
 * @param {Object} props.teacherData - Data of the teacher to be assigned.
 * @param {string} props.teacherData.name - Name of the teacher.
 * @param {Array<string>} props.teacherData.subjects - List of subjects the teacher can teach.
 * @param {string} props.teacherData.id - ID of the teacher.
 *
 * @returns {JSX.Element} The AdminAssignTeacher component.
 *
 * @example
 * <AdminAssignTeacher
 *   isEditOpen={true}
 *   toggleEditProfile={toggleEditProfileFunction}
 *   teacherData={{ name: 'John Doe', subjects: ['Math', 'Science'], id: '123' }}
 * />
 */
const AdminAssignTeacher = ({ isEditOpen, toggleEditProfile, teacherData }) => {
    const [teachers, setTeachers] = useState({ name: '', subjects: [] });
    const [classGrade, setClassGrade] = useState('');
    const [selectedSection, setSelectedSection] = useState([]);
    const [subjects, setSubjects] = useState([]);
    const [currentYear] = useState(new Date().getFullYear());
    const [selectedYear, setSelectedYear] = useState("2024/25");


    /**
     * @function useEffect
     * @description React hook to fetch teacher data.
     */
    useEffect(() => {
        if (!teacherData || Object.keys(teacherData).length === 0) return;
        const data = {
            name: teacherData.name || '',
            subjects: teacherData.subjects || [],
        };

        setTeachers(data);
    }, [teacherData]);

    /**
     * @function handleAssign
     * @description Handles the form submission to assign a teacher to classes.
     * @param {Event} e - The form submission event.
     */
    const handleAssign = async (e) => {
        e.preventDefault();

        try {
            const response = await adminApi.assignTeacher({
                teacher_id: teacherData.id,
                grade: classGrade,
                section: selectedSection,
                subjects_taught: subjects,
                mark_list_year: selectedYear,
            });
            toast.success(response.data['message'], {
                description: currentTime,
                style: { color: 'green' }
            });
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
    const handleYearChange = e => setSelectedYear(e.target.value);

    /**
    * @function handleSectionChange
    * @description Handles the change event for the section selection.
    * @param {Event} e - The change event.
     */
    const handleSectionChange = (e) => {
        const { value, checked } = e.target;
        if (checked) {
            setSelectedSection([...selectedSection, value]);
        } else {
            setSelectedSection(selectedSection.filter((section) => section !== value));
        }
    };

    return (
        <div className={`popup-overlay ${isEditOpen ? "open" : "close"}`}>
            <div className='popup-overlay-container'>
                <div className="close-popup">
                    <h2 style={{ margin: 0 }}>Assign Teacher to Classes</h2>
                    <button onClick={toggleEditProfile}><FaTimes size={24} /></button>
                </div>
                <form onSubmit={handleAssign}>
                    <div className="teacher-form-group">
                        <label htmlFor="teacher">Teacher</label>
                        <select
                            id="teacher"
                            name="teacher"
                            value={teachers.name}
                            onChange={(e) => setTeachers({ ...teachers, name: e.target.value })}
                            required
                        >
                            <option
                                key="default"
                                value={teachers.name}>
                                {teachers.name}
                            </option>
                        </select>
                    </div>
                    <div className="teacher-form-group">
                        <label htmlFor="classGrade">Select Class Grade</label>
                        <select
                            id="classGrade"
                            name="classGrade"
                            value={classGrade}
                            onChange={(e) => setClassGrade(e.target.value)}
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
                    <div className="form-group subjects">
                        <label htmlFor="section">Section:</label>
                        <div className="checkbox-group">
                            {['A', 'B', 'C'].map((section) => (
                                <div className="subject-container" key={section}>
                                    <label>
                                        <input
                                            type="checkbox"
                                            value={section}
                                            checked={selectedSection.includes(section)}
                                            onChange={handleSectionChange}
                                        />
                                        {section}
                                    </label>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="teacher-form-group">
                        <label htmlFor="year">Year:</label>
                        <select id="year" value={selectedYear} onChange={handleYearChange}>
                            {/* Dynamic Year Options */}
                            {Array.from({ length: 3 }, (_, i) => currentYear - i).map(year => (
                                <option key={year} value={year}>
                                    {year}/{(year + 1) % 100}
                                </option>
                            ))}
                        </select>
                    </div>
                    <div className="teacher-form-group">
                        <label htmlFor="subjects">Select Subjects</label>
                        <select
                            id="subjects"
                            name="subjects"
                            value={subjects}
                            onChange={(e) => setSubjects(Array.from(e.target.selectedOptions, option => option.value))}
                            required
                            multiple
                        >
                            {(teachers.subjects && teachers.subjects.length > 0) ? (
                                teachers.subjects.map((subject, index) => (
                                    <option key={index} value={subject}>
                                        {subject}
                                    </option>
                                ))
                            ) : (
                                <option disabled>No subjects available</option>
                            )}
                        </select>
                    </div>
                    <button type="submit" className="teacher-assign-btn">
                        Assign Teacher
                    </button>
                </form>
            </div>
        </div>

    );
};

export default AdminAssignTeacher;
