import { useEffect, useState } from "react";

/**
 * @function assignTeacherData
 * @description Assigns the teacher data to the teacher object.
 * @param {object} data - The teacher data object.
 * @returns {object} The teacher object with the assigned data.
 */
function assignTeacherData(data) {
  if (!data || Object.keys(data).length === 0)
    return {};
  return {
    name: data.name || "",
    age: data.age || 0,
    experience: data.experience || "",
    classes: data.record || [],
    pictureUrl: "https://example.com/teacher-picture.jpg",
    email: data.email || "",
    phone: data.phone || "",
    qualifications: data.qualifications || [],
    subjects: data.subjects || [],
  };
}

/**
 * TeachProfile component displays detailed information about a teacher.
 *
 * @param {object} props - The properties object.
 * @param {boolean} props.isDetailOpen - Indicates if the detail profile is open.
 * @param {Function} props.toggleDetailProfile - Function to toggle the detail profile visibility.
 * @param {object} props.teacherData - The data of the teacher to be displayed.
 *
 * @returns {JSX.Element} The rendered TeachProfile component.
 */
function AdminTeacherProfile({ teacherData }) {
  const [teacher, setTeacher] = useState({
    name: "",
    age: null,
    email: "",
    phone: "",
    experience: "",
    subjects: [],
    classes: [],
    pictureUrl: "https://example.com/teacher-picture.jpg",
    qualifications: [],
  });

  /**
   * Updates the teacher data when the teacherData prop changes.
   */
  useEffect(() => {
    if (teacherData) {
      const transformedData = assignTeacherData(teacherData);
      setTeacher(transformedData);
    }
  }, [teacherData]);

  return (
    <>
      <div className="flex mb-5">
        <div className="mr-5">
          <img
            className=" w-[150px] h-[150px] object-cover rounded-[50%]"
            src={teacher.pictureUrl}
            alt="Teacher"
          />
        </div>
        <div className="flex-1">
          <h2 className="mt-0 mb-2.5 mx-0">{teacher.name}</h2>
          <p>
            Age:
            {teacher.age}
          </p>
          <p>
            Experience:
            {teacher.experience}
          </p>
          <p>
            Email:
            {teacher.email}
          </p>
          <p>
            Phone:
            {teacher.phone}
          </p>
        </div>
      </div>

      <div className="mb-3">
        <h3>Subjects Taught</h3>
        <ul>
          {teacher.subjects
            && teacher.subjects.map((subject, index) => (
              <li key={index}>{subject}</li>
            ))}
        </ul>

        <h3>Classes Handled</h3>
        <ul>
          {teacher.classes && teacher.classes.length > 0
            ? (
                teacher.classes.map((cls, index) => (
                  <li key={index}>
                    Grade:
                    {" "}
                    {cls.grade}
                    , Section:
                    {" "}
                    {cls.section}
                    , Subject:
                    {" "}
                    {cls.subject}
                  </li>
                ))
              )
            : (
                <li key="N/A">N/A</li>
              )}
        </ul>
        <h3>Qualifications</h3>
        <ul>
          {teacher.qualifications
            && teacher.qualifications.map((qualification, index) => (
              <li key={index}>{qualification}</li>
            ))}
        </ul>
      </div>
    </>
  );
}

export default AdminTeacherProfile;
