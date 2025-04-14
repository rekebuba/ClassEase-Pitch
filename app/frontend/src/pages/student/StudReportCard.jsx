import { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { Layout } from "@/components/layout";
import { sharedApi } from "@/api";
import { toast } from "sonner"
import { CollapsibleTable } from '@/features/admin';


const StudentReportCard = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const student_id = queryParams.get('student_id');
    const grade_id = queryParams.get('grade_id');
    const year = queryParams.get('year');
    const [studentAssessment, setStudentAssessment] = useState([]);
    const [studentReport, setStudentReport] = useState([]);


    useEffect(() => {
        const lodeStudentSubjectList = async () => {
            try {
                const response = await sharedApi.getStudentAssessment({
                    student_id: student_id,
                    grade_id: grade_id,
                    year: year
                });
                setStudentAssessment(response.data.assessment);
                setStudentReport(response.data.summary)
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
        lodeStudentSubjectList();
    }, [student_id, grade_id, year]);

    return (
        <Layout role="student">
            {studentAssessment &&
                (<CollapsibleTable studentAssessment={studentAssessment} studentReport={studentReport} />)
            }
        </Layout>
    );
};

export default StudentReportCard;
