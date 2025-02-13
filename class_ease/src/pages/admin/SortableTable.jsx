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
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import api from '../../services/api';

function createData(index, subject, semITotal, semIRank, semIITotal, semIIRank, avgTotal, avgRank) {
    return {
        index,
        subject,
        semITotal,
        semIRank,
        semIITotal,
        semIIRank,
        avgTotal,
        avgRank,
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

function Row(row, studentAssessment) {
    const [open, setOpen] = React.useState(false);

    React.useEffect(() => {
        const assessmentReport = async () => {
            try {
                const res = await api.get('/admin/student/assessment/report', {
                    params: {
                        student_id: assessmentSummary.student_id,
                        grade_id: assessmentSummary.grade_id,
                        subject_id: assessmentSummary.subject_id,
                        section_id: assessmentSummary.section_id,
                        year: assessmentSummary.year,
                    },
                });
                if (res.status === 200) {
                    console.log(res.data);
                    // setAssessmentData(res.data);
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
        assessmentReport()
    }, [assessmentSummary]);

    return (
        <React.Fragment>
            <TableRow sx={{ '& > *': { borderBottom: 'unset' } }}>
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={() => setOpen(!open)}
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
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
                    <Collapse in={open} timeout="auto" unmountOnExit>
                        <Box sx={{ margin: 1 }}>
                            <Typography variant="h6" gutterBottom component="div">
                                History
                            </Typography>
                            <Table size="small" aria-label="purchases">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Date</TableCell>
                                        <TableCell>Customer</TableCell>
                                        <TableCell align="center">Amount</TableCell>
                                        <TableCell align="center">Total price ($)</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {row.history.map((historyRow) => (
                                        <TableRow key={historyRow.date}>
                                            <TableCell component="th" scope="row">
                                                {historyRow.date}
                                            </TableCell>
                                            <TableCell>{historyRow.customerId}</TableCell>
                                            <TableCell align="center">{historyRow.amount}</TableCell>
                                            <TableCell align="center">
                                                hi
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
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
    }).isRequired,
};


export default function CollapsibleTable(studentAssessment) {
    const [rows, setRows] = React.useState([]);

    React.useEffect(() => {
        if (studentAssessment && studentAssessment.studentAssessment) {
            setRows(studentAssessment.studentAssessment.map((assessment, index) => createData(index, assessment.subject, assessment.semI.total, assessment.semI.rank, assessment.semII.total, assessment.semII.rank, assessment.avg_total, assessment.avg_rank)));
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
                        <Row key={row.subject} row={row} studentAssessment={studentAssessment} />
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
}
