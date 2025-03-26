import { useState, useEffect } from 'react';
import { StudentLayout } from "@/components/layout";
import { useNavigate } from 'react-router-dom';
import { studentApi } from '@/api';
import { toast } from "sonner";
import { CourseTable } from "@/features/student/tables"

const StudentCourseRegistration = () => {
    const [courses, setCourses] = useState({});
    const navigate = useNavigate();


    // Mock initial data
    useEffect(() => {
        const fetchCourse = async () => {
            try {
                const response = await studentApi.getCoursesToRegister();
                if (response.status === 200) {
                    setCourses(response.data);
                };
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
        fetchCourse();
    }, []);

    return (
        <StudentLayout>
            <div className="flex flex-col justify-between items-center p-5">
                <h3 className="text-xl font-bold">Student: abc</h3>
                <h3 className="text-xl font-bold">Register For Grade {courses['grade']}</h3>
                <h3 className="text-xl font-bold"> Semester: {courses['semester']}, {courses['academicYear']}</h3>
            </div>
            <CourseTable courses={courses['courses']} />
        </StudentLayout>
    )

};

export default StudentCourseRegistration;
