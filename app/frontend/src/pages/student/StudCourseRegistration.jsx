import { useState, useEffect } from 'react';
import { StudentLayout } from "@/components/layout";
import { useNavigate } from 'react-router-dom';
import { studentApi } from '@/api';
import { toast } from "sonner"
import { CourseTable } from "@/features/student/tables"

const StudentCourseRegistration = () => {
    const [courses, setEvents] = useState([]);
    const navigate = useNavigate();


    // Mock initial data
    useEffect(() => {
        const fetchCourse = async () => {
            try {
                const response = await studentApi.getCoursesToRegister();
                if (response.status === 200) {
                    setEvents(response.data['course']);
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
            <div className="flex justify-between items-center p-5">
                <h1 className="text-2xl font-bold">List of Course To Register</h1>
            </div>
            <CourseTable courses={courses} />
        </StudentLayout>
    )

};

export default StudentCourseRegistration;
