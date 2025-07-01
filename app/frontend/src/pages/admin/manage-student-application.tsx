"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import {
    Eye,
    Users,
    Clock,
    CheckCircle,
    XCircle,
    FileText,
    GraduationCap,
    MapPin,
    Phone,
    Mail,
    Heart,
    AlertTriangle,
    Bus,
    Utensils,
    Activity,
} from "lucide-react"
import type { StudentApplication } from "@/lib/api-validation"
import { Layout, StudentStatusBadge } from "@/components"
import { StudentDetailDialog } from "@/components"

// Mock data - in real app this would come from your backend
const mockStudents: StudentApplication[] = [
    {
        id: "1",
        registrationDate: "2024-01-15",
        status: "pending",
        firstName: "Emma",
        fatherName: "Michael Johnson",
        grandFatherName: "Robert Johnson",
        dateOfBirth: "2015-03-22",
        gender: "female",
        nationality: "American",
        bloodType: "A+",
        grade: "Grade 3",
        academicYear: "2024-2025",
        isTransfer: false,
        transportation: "school-bus",
        address: "123 Oak Street",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62701",
        fatherPhone: "(555) 123-4567",
        motherPhone: "(555) 987-6543",
        parentEmail: "johnson.family@email.com",
        guardianName: "Sarah Johnson",
        guardianPhone: "(555) 111-2222",
        guardianRelation: "aunt-uncle",
        emergencyContactName: "Patricia Williams",
        emergencyContactPhone: "(555) 333-4444",
        siblingInSchool: true,
        siblingDetails: "Brother: Alex Johnson in Grade 5",
        hasMedicalCondition: false,
        hasDisability: false,
    },
    {
        id: "2",
        registrationDate: "2024-01-18",
        status: "under-review",
        firstName: "Liam",
        fatherName: "David Chen",
        dateOfBirth: "2013-07-14",
        gender: "male",
        nationality: "American",
        bloodType: "B+",
        grade: "Grade 5",
        academicYear: "2024-2025",
        isTransfer: true,
        previousSchool: "Roosevelt Elementary",
        previousGrades: "Excellent performance, honor roll student",
        transportation: "parent-drop",
        address: "456 Pine Avenue",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62702",
        fatherPhone: "(555) 234-5678",
        motherPhone: "(555) 876-5432",
        parentEmail: "chen.family@email.com",
        emergencyContactName: "Lisa Chen",
        emergencyContactPhone: "(555) 222-3333",
        siblingInSchool: false,
        hasMedicalCondition: true,
        medicalDetails: "Mild asthma, requires inhaler during physical activities",
        hasDisability: false,
    },
    {
        id: "3",
        registrationDate: "2024-01-20",
        status: "documents-required",
        firstName: "Sophia",
        fatherName: "Carlos Rodriguez",
        grandFatherName: "Miguel Rodriguez",
        dateOfBirth: "2016-11-03",
        gender: "female",
        nationality: "American",
        bloodType: "O-",
        grade: "Grade 2",
        academicYear: "2024-2025",
        isTransfer: false,
        transportation: "walk",
        address: "789 Maple Drive",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62703",
        fatherPhone: "(555) 345-6789",
        motherPhone: "(555) 765-4321",
        parentEmail: "rodriguez.family@email.com",
        guardianName: "Maria Rodriguez",
        guardianPhone: "(555) 333-4444",
        guardianRelation: "grandparent",
        emergencyContactName: "Ana Rodriguez",
        emergencyContactPhone: "(555) 444-5555",
        siblingInSchool: false,
        hasMedicalCondition: false,
        hasDisability: true,
        disabilityDetails: "Mild hearing impairment in left ear",
    },
    {
        id: "4",
        registrationDate: "2024-01-22",
        status: "approved",
        firstName: "Noah",
        fatherName: "James Thompson",
        dateOfBirth: "2012-05-18",
        gender: "male",
        nationality: "American",
        bloodType: "AB+",
        grade: "Grade 6",
        academicYear: "2024-2025",
        isTransfer: false,
        transportation: "bicycle",
        address: "321 Elm Street",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62704",
        fatherPhone: "(555) 456-7890",
        motherPhone: "(555) 654-3210",
        parentEmail: "thompson.family@email.com",
        emergencyContactName: "Jennifer Thompson",
        emergencyContactPhone: "(555) 777-8888",
        siblingInSchool: true,
        siblingDetails: "Sister: Olivia Thompson in Grade 4",
        hasMedicalCondition: false,
        hasDisability: false,
    },
    {
        id: "5",
        registrationDate: "2024-01-25",
        status: "enrolled",
        firstName: "Ava",
        fatherName: "Robert Anderson",
        dateOfBirth: "2017-09-12",
        gender: "female",
        nationality: "American",
        bloodType: "A-",
        grade: "Grade 1",
        academicYear: "2024-2025",
        isTransfer: false,
        transportation: "school-bus",
        address: "654 Cedar Lane",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62705",
        fatherPhone: "(555) 567-8901",
        motherPhone: "(555) 543-2109",
        parentEmail: "anderson.family@email.com",
        emergencyContactName: "Susan Anderson",
        emergencyContactPhone: "(555) 999-0000",
        siblingInSchool: false,
        hasMedicalCondition: false,
        hasDisability: false,
    },
    {
        id: "6",
        registrationDate: "2024-01-28",
        status: "rejected",
        firstName: "Ethan",
        fatherName: "Mark Wilson",
        dateOfBirth: "2014-12-08",
        gender: "male",
        nationality: "American",
        grade: "Grade 4",
        academicYear: "2024-2025",
        isTransfer: true,
        previousSchool: "Lincoln Elementary",
        previousGrades: "Below average performance, behavioral concerns",
        transportation: "parent-drop",
        address: "987 Birch Road",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62706",
        fatherPhone: "(555) 678-9012",
        motherPhone: "(555) 432-1098",
        parentEmail: "wilson.family@email.com",
        emergencyContactName: "Carol Wilson",
        emergencyContactPhone: "(555) 000-1111",
        siblingInSchool: false,
        hasMedicalCondition: true,
        medicalDetails: "ADHD, requires medication management and behavioral support",
        hasDisability: true,
        disabilityDetails: "Learning disability in reading comprehension",
    },
]

export default function ManageStudentsApplication() {
    const [students, setStudents] = useState<StudentApplication[]>(mockStudents)
    const [selectedStudent, setSelectedStudent] = useState<StudentApplication | null>(null)
    const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false)

    const handleViewDetails = (student: StudentApplication) => {
        setSelectedStudent(student)
        setIsDetailDialogOpen(true)
    }

    const handleStatusChange = (studentId: string, newStatus: StudentApplication["status"]) => {
        setStudents((prev) =>
            prev.map((student) => (student.id === studentId ? { ...student, status: newStatus } : student)),
        )
    }

    const getStatusCounts = () => {
        return students.reduce(
            (acc, student) => {
                acc[student.status] = (acc[student.status] || 0) + 1
                return acc
            },
            {} as Record<string, number>,
        )
    }

    const statusCounts = getStatusCounts()

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
            day: "numeric",
        })
    }

    const getInitials = (firstName: string, fatherName: string) => {
        return `${firstName.charAt(0)}${fatherName.charAt(0)}`.toUpperCase()
    }

    const calculateAge = (dateOfBirth: string) => {
        const today = new Date()
        const birthDate = new Date(dateOfBirth)
        let age = today.getFullYear() - birthDate.getFullYear()
        const monthDiff = today.getMonth() - birthDate.getMonth()
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
            age--
        }
        return age
    }

    const getGradeLevel = (grade: string) => {
        const gradeMap: Record<string, string> = {
            KG: "KG",
            "Grade 1": "1st",
            "Grade 2": "2nd",
            "Grade 3": "3rd",
            "Grade 4": "4th",
            "Grade 5": "5th",
            "Grade 6": "6th",
            "Grade 7": "7th",
            "Grade 8": "8th",
            "Grade 9": "9th",
            "Grade 10": "10th",
            "Grade 11": "11th",
            "Grade 12": "12th",
        }
        return gradeMap[grade] || grade
    }

    return (
        <Layout role="admin">
            <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-100 p-6">
                <div className="max-w-7xl mx-auto space-y-6">
                    {/* Header */}
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">Student Registrations</h1>
                            <p className="text-gray-600 mt-1">Manage and review student registration applications</p>
                        </div>
                        <div className="flex items-center gap-2">
                            <Badge variant="outline" className="text-lg px-3 py-1">
                                {students.length} Total Registrations
                            </Badge>
                        </div>
                    </div>
                    {/* Status Overview Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Pending</CardTitle>
                                <Clock className="h-4 w-4 text-yellow-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-yellow-600">{statusCounts.pending || 0}</div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Under Review</CardTitle>
                                <Eye className="h-4 w-4 text-blue-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-blue-600">{statusCounts["under-review"] || 0}</div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Documents Required</CardTitle>
                                <FileText className="h-4 w-4 text-orange-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-orange-600">{statusCounts["documents-required"] || 0}</div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Approved</CardTitle>
                                <CheckCircle className="h-4 w-4 text-green-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-green-600">{statusCounts.approved || 0}</div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Enrolled</CardTitle>
                                <GraduationCap className="h-4 w-4 text-purple-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-purple-600">{statusCounts.enrolled || 0}</div>
                            </CardContent>
                        </Card>
                        <Card>
                            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                                <CardTitle className="text-sm font-medium">Rejected</CardTitle>
                                <XCircle className="h-4 w-4 text-red-600" />
                            </CardHeader>
                            <CardContent>
                                <div className="text-2xl font-bold text-red-600">{statusCounts.rejected || 0}</div>
                            </CardContent>
                        </Card>
                    </div>
                    {/* Students Table */}
                    <Card>
                        <CardHeader>
                            <div className="flex justify-between items-center">
                                <div>
                                    <CardTitle className="flex items-center gap-2">
                                        <Users className="h-5 w-5" />
                                        Student Registrations
                                    </CardTitle>
                                    <CardDescription>Review and manage all student registration applications</CardDescription>
                                </div>
                                <Button onClick={() => {
                                    // Navigate to new application page
                                    window.location.href = "/admin/student/registration/new"
                                }} className="bg-blue-600 text-white hover:bg-blue-700">
                                    New Application
                                </Button>
                            </div>
                        </CardHeader>
                        <CardContent>
                            <div className="rounded-md border">
                                <Table>
                                    <TableHeader>
                                        <TableRow>
                                            <TableHead className="w-[250px]">Student</TableHead>
                                            <TableHead>Grade & Academic</TableHead>
                                            <TableHead>Family Contact</TableHead>
                                            <TableHead>Medical & Special Needs</TableHead>
                                            <TableHead>Status</TableHead>
                                            <TableHead>Registration</TableHead>
                                            <TableHead>Flags</TableHead>
                                            <TableHead>Actions</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        {students.map((student) => (
                                            <TableRow key={student.id} className="hover:bg-gray-50">
                                                <TableCell>
                                                    <div className="flex items-center gap-3">
                                                        <Avatar className="h-10 w-10">
                                                            <AvatarImage src={student.studentPhoto || "/placeholder.svg"} />
                                                            <AvatarFallback>{getInitials(student.firstName, student.fatherName)}</AvatarFallback>
                                                        </Avatar>
                                                        <div>
                                                            <div className="font-medium">
                                                                {student.firstName} {student.fatherName}
                                                            </div>
                                                            <div className="text-sm text-gray-500">Age: {calculateAge(student.dateOfBirth)}</div>
                                                            {student.bloodType && (
                                                                <div className="text-sm text-gray-500">Blood: {student.bloodType}</div>
                                                            )}
                                                        </div>
                                                    </div>
                                                </TableCell>
                                                <TableCell>
                                                    <div>
                                                        <Badge className="bg-blue-100 text-blue-800 mb-1">{getGradeLevel(student.grade)}</Badge>
                                                        <div className="text-sm text-gray-500">{student.academicYear}</div>
                                                        {student.isTransfer && (
                                                            <Badge variant="outline" className="bg-orange-100 text-orange-800 text-xs">
                                                                Transfer
                                                            </Badge>
                                                        )}
                                                        <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                                                            <MapPin className="h-3 w-3" />
                                                            {student.city}, {student.state}
                                                        </div>
                                                    </div>
                                                </TableCell>
                                                <TableCell>
                                                    <div className="space-y-1">
                                                        <div className="flex items-center gap-1 text-sm">
                                                            <Phone className="h-3 w-3 text-gray-500" />
                                                            <span>{student.fatherPhone}</span>
                                                        </div>
                                                        <div className="flex items-center gap-1 text-sm">
                                                            <Phone className="h-3 w-3 text-gray-500" />
                                                            <span>{student.motherPhone}</span>
                                                        </div>
                                                        <div className="flex items-center gap-1 text-sm">
                                                            <Mail className="h-3 w-3 text-gray-500" />
                                                            <span className="truncate max-w-[120px]">{student.parentEmail}</span>
                                                        </div>
                                                        {student.siblingInSchool && (
                                                            <Badge variant="outline" className="text-xs">
                                                                Has Sibling
                                                            </Badge>
                                                        )}
                                                    </div>
                                                </TableCell>
                                                <TableCell>
                                                    <div className="space-y-1">
                                                        {student.hasMedicalCondition && (
                                                            <Badge variant="destructive" className="text-xs flex items-center gap-1 w-fit">
                                                                <Heart className="h-3 w-3" />
                                                                Medical
                                                            </Badge>
                                                        )}
                                                        {student.hasDisability && (
                                                            <Badge variant="destructive" className="text-xs flex items-center gap-1 w-fit">
                                                                <AlertTriangle className="h-3 w-3" />
                                                                Disability
                                                            </Badge>
                                                        )}
                                                        {!student.hasMedicalCondition &&
                                                            !student.hasDisability && (
                                                                <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1 w-fit">
                                                                    <CheckCircle className="h-3 w-3" />
                                                                    Healthy
                                                                </Badge>
                                                            )}
                                                    </div>
                                                </TableCell>
                                                <TableCell>
                                                    <StudentStatusBadge status={student.status} />
                                                </TableCell>
                                                <TableCell>
                                                    <div className="text-sm">{formatDate(student.registrationDate)}</div>
                                                    {student.isTransfer && student.previousSchool && (
                                                        <div className="text-xs text-gray-500">From: {student.previousSchool}</div>
                                                    )}
                                                </TableCell>
                                                <TableCell>
                                                    <div className="flex flex-col gap-1">
                                                        {student.isTransfer && (
                                                            <Badge variant="outline" className="text-xs">
                                                                Transfer
                                                            </Badge>
                                                        )}
                                                        {(student.hasMedicalCondition || student.hasDisability) && (
                                                            <Badge variant="destructive" className="text-xs flex items-center gap-1">
                                                                <AlertTriangle className="h-3 w-3" />
                                                                Needs Attention
                                                            </Badge>
                                                        )}
                                                        {!student.hasMedicalCondition &&
                                                            !student.hasDisability &&
                                                            !student.isTransfer && (
                                                                <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1">
                                                                    <CheckCircle className="h-3 w-3" />
                                                                    Standard
                                                                </Badge>
                                                            )}
                                                    </div>
                                                </TableCell>
                                                <TableCell className="text-right">
                                                    <Button
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => handleViewDetails(student)}
                                                        className="flex items-center gap-1"
                                                    >
                                                        <Eye className="h-4 w-4" />
                                                        View Details
                                                    </Button>
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </div>
                        </CardContent>
                    </Card>
                    {/* Student Detail Dialog */}
                    <StudentDetailDialog
                        student={selectedStudent}
                        isOpen={isDetailDialogOpen}
                        onClose={() => {
                            setIsDetailDialogOpen(false)
                            setSelectedStudent(null)
                        }}
                        onStatusChange={handleStatusChange}
                    />
                </div>
            </div>
        </Layout>
    )
}
