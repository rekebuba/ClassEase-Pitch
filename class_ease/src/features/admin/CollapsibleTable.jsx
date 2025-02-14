import * as React from 'react';
import PropTypes from 'prop-types';
import Box from '@mui/material/Box';
import Collapse from '@mui/material/Collapse';
import IconButton from '@mui/material/IconButton';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { api } from '@/api';
import { toast } from "sonner"

function createData(index, subject, semITotal, semIRank, semIITotal, semIIRank, avgTotal, avgRank, studentId, gradeId, subjectId, year) {
    return {
        index,
        subject,
        semITotal,
        semIRank,
        semIITotal,
        semIIRank,
        avgTotal,
        avgRank,
        studentId,
        gradeId,
        subjectId,
        year,
        history: [
            {
                date: '2020-01-05',
                customerId: '11091700',
                amount: 3,
            },
            {
                date: '2020-01-02',
                customerId: 'Anonymous',
                amount: 1,
            },
        ],
    };
}

function Row(props) {
    const { row } = props;
    const [open, setOpen] = React.useState(false);
    const [detailAssessment, setDetailAssessment] = React.useState();

    const assessmentReport = async () => {
        try {
            const res = await api.get('/admin/student/assessment/report', {
                params: {
                    student_id: row.studentId,
                    grade_id: row.gradeId,
                    subject_id: row.subjectId,
                    year: row.year,
                },
            });
            if (res.status === 200) {
                setDetailAssessment(res.data)
            }
        } catch (error) {
            if (error.response?.data?.error) {
                toast.error(error.response.data['error'], {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            }
        }
    }

    const handleOpen = async () => {
        await assessmentReport()
        setOpen(!open)
    }

    return (
        <React.Fragment>
            <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}
            className={`bg-${row.index % 2 === 0 ? 'white' : 'gray-100'} hover:bg-gray-200`}
            >
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        // onClick={() => setOpen(!open)}
                        onClick={handleOpen}

                    >
                        {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell align="center">{row.index + 1}</TableCell>
                <TableCell align="center">{row.subject}</TableCell>
                <TableCell align="center">{row.semITotal}</TableCell>
                <TableCell align="center">{row.semIRank}</TableCell>
                <TableCell align="center">{row.semIITotal}</TableCell>
                <TableCell align="center">{row.semIIRank}</TableCell>
                <TableCell align="center">{row.avgTotal}</TableCell>
                <TableCell align="center">{row.avgRank}</TableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={9}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{ margin: 1 }}>
                            <div className='flex flex-wrap justify-between p-2 gap-10'>
                                {(detailAssessment && Object.entries(detailAssessment).length !== 0) &&
                                    Object.keys(detailAssessment).map((semester) => (
                                        <div key={semester} className='flex-1 p-4 w-96 min-w-[250px] border border-gray-300 rounded-lg shadow-md bg-white'>
                                            <h3 className='text-center text-lg font-bold'>Semester {semester}</h3>
                                            <Table size="small" aria-label="purchases">
                                                <TableHead className='bg-gray-200'>
                                                    <TableRow>
                                                        <TableCell>No.</TableCell>
                                                        <TableCell>Type</TableCell>
                                                        <TableCell align="center">Score</TableCell>
                                                    </TableRow>
                                                </TableHead>
                                                <TableBody>
                                                    {detailAssessment[semester].map((assessment, index) => (
                                                        <TableRow key={index} className={`bg-${index % 2 === 0 ? 'white' : 'gray-100'} hover:bg-gray-200`}>
                                                            <TableCell component="th" scope="row">{index + 1}</TableCell>
                                                            <TableCell>{assessment.assessment_type}</TableCell>
                                                            <TableCell align="center">{assessment.score}</TableCell>
                                                        </TableRow>
                                                    ))}
                                                </TableBody>
                                            </Table>
                                            <div className='text-right text-lg p-2'>
                                                <h3><strong>Total: {semester == 1 ? row.semITotal : row.semIITotal} / 100</strong></h3>
                                            </div>
                                        </div>
                                    ))}
                            </div>
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </React.Fragment>
    );
}

Row.propTypes = {
    row: PropTypes.shape({
        index: PropTypes.number.isRequired,
        avgRank: PropTypes.number.isRequired,
        avgTotal: PropTypes.number.isRequired,
        history: PropTypes.arrayOf(
            PropTypes.shape({
                amount: PropTypes.number.isRequired,
                customerId: PropTypes.string.isRequired,
                date: PropTypes.string.isRequired,
            }),
        ).isRequired,
        semIIRank: PropTypes.number.isRequired,
        semIITotal: PropTypes.number.isRequired,
        semIRank: PropTypes.number.isRequired,
        semITotal: PropTypes.number.isRequired,
        subject: PropTypes.string.isRequired,
        studentId: PropTypes.string.isRequired,
        subjectId: PropTypes.string.isRequired,
        gradeId: PropTypes.string.isRequired,
        year: PropTypes.string.isRequired,

    }).isRequired,
};


export default function CollapsibleTable(props) {
    const [rows, setRows] = React.useState([]);
    const { studentAssessment, studentReport } = props;

    React.useEffect(() => {
        if (studentAssessment) {
            setRows(studentAssessment.map((assessment, index) => {
                return createData(index,
                    assessment.subject,
                    assessment.semI.total,
                    assessment.semI.rank,
                    assessment.semII.total,
                    assessment.semII.rank,
                    assessment.avg_total,
                    assessment.avg_rank,
                    assessment.student_id,
                    assessment.grade_id,
                    assessment.subject_id,
                    assessment.year
                )
            }));
        }
    }, [studentAssessment]);


    return (
        <TableContainer component={Paper}>
            <Table aria-label="collapsible table" className='bg-gray-100'>
                <TableHead className='bg-gray-200'>
                    <TableRow>
                        <TableCell />
                        <TableCell>No.</TableCell>
                        <TableCell align="center">Subject</TableCell>
                        <TableCell align="center">Sem I Total</TableCell>
                        <TableCell align="center">Sem I Rank</TableCell>
                        <TableCell align="center">Sem II Total</TableCell>
                        <TableCell align="center">Sem II Rank</TableCell>
                        <TableCell align="center">Average Total</TableCell>
                        <TableCell align="center">Average Rank</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {rows.map((row) => (
                        <Row key={row.subject} row={row} />
                    ))}
                    {studentReport &&
                        <TableRow>
                            <TableCell colSpan={9}>
                                <div className="flex justify-between items-center px-6 mr-28">
                                    {/* Total Section */}
                                    <div className="text-lg font-semibold text-gray-700">Total</div>
                                    {studentReport.semesters && studentReport.semesters.map((semester, index) => (
                                        <React.Fragment key={index}>
                                            {/* Semester I Section */}
                                            <div className="text-center">
                                                <div className="text-sm font-medium text-gray-600">Semester {semester.semester}</div>
                                                <div className="text-lg font-bold text-gray-800">{semester.semester_average}</div>
                                                <div className="text-sm text-gray-500">Rank: {semester.semester_rank}</div>
                                            </div>
                                        </React.Fragment>
                                    ))}
                                    {/* Average Section */}
                                    <div className="text-center">
                                        <div className="text-sm font-medium text-gray-600">Average</div>
                                        <div className="text-lg font-bold text-green-600">{studentReport.final_score}</div>
                                        <div className="text-sm text-gray-500">Rank: {studentReport.final_rank}</div>
                                    </div>
                                </div>
                                <div className="flex justify-between items-center px-6 mr-28 mt-5">
                                    {/* status */}
                                    <div className="text-lg font-semibold text-gray-700">Academic Status: <span className="text-lg font-bold text-green-600">Pending</span></div>
                                </div>
                            </TableCell>
                        </TableRow>
                    }
                </TableBody>
            </Table>
        </TableContainer >
    );
}
