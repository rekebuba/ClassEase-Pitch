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
    Calendar,
    GraduationCap,
    MapPin,
    Phone,
    Mail,
    Award,
    AlertTriangle,
} from "lucide-react"
import type { TeacherApplication } from "@/lib/api-validation"
import { TeacherStatusBadge } from "@/components"
import { TeacherDetailDialog } from "@/components"

// Mock data - in real app this would come from your backend
const mockTeachers: TeacherApplication[] = [
    {
        id: "1",
        applicationDate: "2024-01-15",
        status: "pending",
        firstName: "Sarah",
        middleName: "Jane",
        lastName: "Johnson",
        preferredName: "Sarah",
        dateOfBirth: "1985-03-22",
        gender: "female",
        nationality: "American",
        maritalStatus: "married",
        address: "123 Oak Street",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62701",
        country: "United States",
        primaryPhone: "(555) 123-4567",
        secondaryPhone: "(555) 987-6543",
        personalEmail: "sarah.johnson@email.com",
        workEmail: "s.johnson@school.edu",
        emergencyContactName: "Michael Johnson",
        emergencyContactRelation: "Spouse",
        emergencyContactPhone: "(555) 111-2222",
        highestDegree: "masters",
        majorSubject: "Elementary Education",
        minorSubject: "Psychology",
        university: "University of Illinois",
        graduationYear: "2008",
        gpa: "3.8",
        teachingLicense: true,
        licenseNumber: "IL-12345678",
        licenseState: "Illinois",
        licenseExpirationDate: "2025-06-30",
        certifications: ["ESL Certification", "Reading Specialist"],
        specializations: ["Special Needs Education", "STEM Education"],
        yearsOfExperience: "11-15",
        previousSchools: "Lincoln Elementary (2008-2015), Washington Middle School (2015-2020)",
        subjectsToTeach: ["Mathematics", "English Language Arts", "Science"],
        gradeLevelsToTeach: ["Grade 3", "Grade 4", "Grade 5"],
        preferredSchedule: "full-time",
        languagesSpoken: ["English", "Spanish"],
        technologySkills: ["Microsoft Office", "Google Workspace", "Learning Management Systems"],
        specialSkills: "Excellent classroom management, experience with diverse learners",
        positionApplyingFor: "Elementary Teacher",
        departmentPreference: "Elementary",
        availableStartDate: "2024-08-15",
        salaryExpectation: "$55,000",
        willingToRelocate: false,
        hasTransportation: true,
        hasConvictions: false,
        hasDisciplinaryActions: false,
        reference1Name: "Dr. Patricia Williams",
        reference1Title: "Principal",
        reference1Organization: "Lincoln Elementary School",
        reference1Phone: "(555) 333-4444",
        reference1Email: "p.williams@lincoln.edu",
        reference2Name: "James Miller",
        reference2Title: "Department Head",
        reference2Organization: "Washington Middle School",
        reference2Phone: "(555) 555-6666",
        reference2Email: "j.miller@washington.edu",
        teachingPhilosophy:
            "I believe every child can learn and succeed with the right support and encouragement. My approach focuses on creating an inclusive, engaging environment where students feel safe to explore and make mistakes as part of their learning journey.",
        whyTeaching:
            "Teaching allows me to make a positive impact on young minds and help shape the future. I'm passionate about helping students discover their potential and develop a love for learning.",
        resume: "sarah_johnson_resume.pdf",
        coverLetter: "sarah_johnson_cover_letter.pdf",
        transcripts: "sarah_johnson_transcripts.pdf",
        teachingCertificate: "sarah_johnson_certificate.pdf",
    },
    {
        id: "2",
        applicationDate: "2024-01-18",
        status: "under-review",
        firstName: "Michael",
        lastName: "Chen",
        dateOfBirth: "1990-07-14",
        gender: "male",
        nationality: "American",
        maritalStatus: "single",
        address: "456 Pine Avenue",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62702",
        country: "United States",
        primaryPhone: "(555) 234-5678",
        personalEmail: "michael.chen@email.com",
        emergencyContactName: "Lisa Chen",
        emergencyContactRelation: "Sister",
        emergencyContactPhone: "(555) 222-3333",
        highestDegree: "bachelors",
        majorSubject: "Mathematics",
        minorSubject: "Computer Science",
        university: "Northwestern University",
        graduationYear: "2012",
        gpa: "3.9",
        teachingLicense: true,
        licenseNumber: "IL-87654321",
        licenseState: "Illinois",
        licenseExpirationDate: "2026-12-31",
        certifications: ["Technology Integration"],
        specializations: ["STEM Education"],
        yearsOfExperience: "6-10",
        previousSchools: "Roosevelt High School (2012-2020), Jefferson Middle School (2020-2024)",
        subjectsToTeach: ["Mathematics", "Computer Science"],
        gradeLevelsToTeach: ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10"],
        preferredSchedule: "full-time",
        languagesSpoken: ["English", "Chinese"],
        technologySkills: ["Microsoft Office", "Google Workspace", "Coding/Programming", "Educational Software"],
        specialSkills: "Strong analytical skills, experience with educational technology integration",
        positionApplyingFor: "Mathematics Teacher",
        departmentPreference: "Mathematics",
        availableStartDate: "2024-08-20",
        salaryExpectation: "$58,000",
        willingToRelocate: true,
        hasTransportation: true,
        hasConvictions: false,
        hasDisciplinaryActions: false,
        reference1Name: "Dr. Robert Kim",
        reference1Title: "Principal",
        reference1Organization: "Roosevelt High School",
        reference1Phone: "(555) 444-5555",
        reference1Email: "r.kim@roosevelt.edu",
        teachingPhilosophy:
            "Mathematics is everywhere in our daily lives. I strive to make math relevant and accessible to all students by connecting abstract concepts to real-world applications.",
        whyTeaching:
            "I want to inspire the next generation of problem solvers and critical thinkers through mathematics education.",
        resume: "michael_chen_resume.pdf",
        transcripts: "michael_chen_transcripts.pdf",
        teachingCertificate: "michael_chen_certificate.pdf",
    },
    {
        id: "3",
        applicationDate: "2024-01-20",
        status: "interview-scheduled",
        firstName: "Emily",
        lastName: "Rodriguez",
        dateOfBirth: "1988-11-03",
        gender: "female",
        nationality: "American",
        maritalStatus: "divorced",
        address: "789 Maple Drive",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62703",
        country: "United States",
        primaryPhone: "(555) 345-6789",
        personalEmail: "emily.rodriguez@email.com",
        emergencyContactName: "Maria Rodriguez",
        emergencyContactRelation: "Mother",
        emergencyContactPhone: "(555) 333-4444",
        highestDegree: "masters",
        majorSubject: "English Literature",
        university: "University of Chicago",
        graduationYear: "2010",
        gpa: "3.7",
        teachingLicense: true,
        licenseNumber: "IL-11223344",
        licenseState: "Illinois",
        licenseExpirationDate: "2025-08-31",
        certifications: ["ESL Certification", "Reading Specialist"],
        specializations: ["English as Second Language"],
        yearsOfExperience: "11-15",
        previousSchools: "Central High School (2010-2024)",
        subjectsToTeach: ["English Language Arts", "ESL/EFL"],
        gradeLevelsToTeach: ["Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        preferredSchedule: "full-time",
        languagesSpoken: ["English", "Spanish", "French"],
        technologySkills: ["Microsoft Office", "Google Workspace", "Online Assessment Tools"],
        specialSkills: "Bilingual education, cultural sensitivity, curriculum development",
        positionApplyingFor: "English Teacher",
        departmentPreference: "English",
        availableStartDate: "2024-08-15",
        salaryExpectation: "$62,000",
        willingToRelocate: false,
        hasTransportation: true,
        hasConvictions: false,
        hasDisciplinaryActions: false,
        reference1Name: "Dr. Amanda Foster",
        reference1Title: "Department Head",
        reference1Organization: "Central High School",
        reference1Phone: "(555) 666-7777",
        reference1Email: "a.foster@central.edu",
        teachingPhilosophy:
            "Language is the gateway to understanding and expressing our thoughts and emotions. I believe in creating an inclusive environment where all students can develop their communication skills.",
        whyTeaching:
            "I'm passionate about helping students find their voice through literature and writing, especially those from diverse backgrounds.",
        resume: "emily_rodriguez_resume.pdf",
        coverLetter: "emily_rodriguez_cover_letter.pdf",
        transcripts: "emily_rodriguez_transcripts.pdf",
        teachingCertificate: "emily_rodriguez_certificate.pdf",
    },
    {
        id: "4",
        applicationDate: "2024-01-22",
        status: "approved",
        firstName: "David",
        lastName: "Thompson",
        dateOfBirth: "1982-05-18",
        gender: "male",
        nationality: "American",
        maritalStatus: "married",
        address: "321 Elm Street",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62704",
        country: "United States",
        primaryPhone: "(555) 456-7890",
        personalEmail: "david.thompson@email.com",
        emergencyContactName: "Jennifer Thompson",
        emergencyContactRelation: "Spouse",
        emergencyContactPhone: "(555) 777-8888",
        highestDegree: "masters",
        majorSubject: "Physical Education",
        university: "Illinois State University",
        graduationYear: "2005",
        gpa: "3.6",
        teachingLicense: true,
        licenseNumber: "IL-55667788",
        licenseState: "Illinois",
        licenseExpirationDate: "2025-12-31",
        certifications: ["First Aid/CPR", "Coaching Certification"],
        specializations: ["Sports Medicine"],
        yearsOfExperience: "16-20",
        previousSchools: "Westfield High School (2005-2024)",
        subjectsToTeach: ["Physical Education"],
        gradeLevelsToTeach: ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"],
        preferredSchedule: "full-time",
        languagesSpoken: ["English"],
        technologySkills: ["Microsoft Office", "Fitness Tracking Apps"],
        specialSkills: "Athletic coaching, sports injury prevention, team building",
        positionApplyingFor: "Physical Education Teacher",
        departmentPreference: "Physical Education",
        availableStartDate: "2024-08-15",
        salaryExpectation: "$60,000",
        willingToRelocate: false,
        hasTransportation: true,
        hasConvictions: false,
        hasDisciplinaryActions: false,
        reference1Name: "Coach Mark Wilson",
        reference1Title: "Athletic Director",
        reference1Organization: "Westfield High School",
        reference1Phone: "(555) 888-9999",
        reference1Email: "m.wilson@westfield.edu",
        teachingPhilosophy:
            "Physical education is about more than just sports - it's about building character, teamwork, and healthy habits that last a lifetime.",
        whyTeaching:
            "I want to inspire students to lead active, healthy lives and develop confidence through physical activity and sports.",
        resume: "david_thompson_resume.pdf",
        transcripts: "david_thompson_transcripts.pdf",
        teachingCertificate: "david_thompson_certificate.pdf",
    },
    {
        id: "5",
        applicationDate: "2024-01-25",
        status: "rejected",
        firstName: "Lisa",
        lastName: "Anderson",
        dateOfBirth: "1995-09-12",
        gender: "female",
        nationality: "American",
        maritalStatus: "single",
        address: "654 Cedar Lane",
        city: "Springfield",
        state: "Illinois",
        postalCode: "62705",
        country: "United States",
        primaryPhone: "(555) 567-8901",
        personalEmail: "lisa.anderson@email.com",
        emergencyContactName: "Robert Anderson",
        emergencyContactRelation: "Father",
        emergencyContactPhone: "(555) 999-0000",
        highestDegree: "bachelors",
        majorSubject: "Art Education",
        university: "Southern Illinois University",
        graduationYear: "2017",
        gpa: "3.4",
        teachingLicense: false,
        certifications: ["Art Therapy"],
        specializations: ["Arts Integration"],
        yearsOfExperience: "3-5",
        previousSchools: "Community Art Center (2017-2022)",
        subjectsToTeach: ["Art"],
        gradeLevelsToTeach: ["KG", "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"],
        preferredSchedule: "part-time",
        languagesSpoken: ["English"],
        technologySkills: ["Graphic Design", "Digital Art Software"],
        specialSkills: "Creative arts, working with young children, art therapy techniques",
        positionApplyingFor: "Art Teacher",
        departmentPreference: "Arts",
        availableStartDate: "2024-09-01",
        salaryExpectation: "$35,000",
        willingToRelocate: false,
        hasTransportation: true,
        hasConvictions: false,
        hasDisciplinaryActions: false,
        reference1Name: "Susan Clark",
        reference1Title: "Program Director",
        reference1Organization: "Community Art Center",
        reference1Phone: "(555) 000-1111",
        reference1Email: "s.clark@artcenter.org",
        teachingPhilosophy:
            "Art is a universal language that allows students to express themselves and explore their creativity without boundaries.",
        whyTeaching:
            "I believe art education is essential for developing creativity, critical thinking, and emotional expression in children.",
        resume: "lisa_anderson_resume.pdf",
    },
]

export default function TeacherAdminDashboard() {
    const [teachers, setTeachers] = useState<TeacherApplication[]>(mockTeachers)
    const [selectedTeacher, setSelectedTeacher] = useState<TeacherApplication | null>(null)
    const [isDetailDialogOpen, setIsDetailDialogOpen] = useState(false)

    const handleViewDetails = (teacher: TeacherApplication) => {
        setSelectedTeacher(teacher)
        setIsDetailDialogOpen(true)
    }

    const handleStatusChange = (teacherId: string, newStatus: TeacherApplication["status"]) => {
        setTeachers((prev) =>
            prev.map((teacher) => (teacher.id === teacherId ? { ...teacher, status: newStatus } : teacher)),
        )
    }

    const getStatusCounts = () => {
        return teachers.reduce(
            (acc, teacher) => {
                acc[teacher.status] = (acc[teacher.status] || 0) + 1
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

    const getInitials = (firstName: string, lastName: string) => {
        return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
    }

    const getExperienceLevel = (experience: string) => {
        const experienceMap = {
            "0": "New",
            "1-2": "Entry",
            "3-5": "Junior",
            "6-10": "Mid",
            "11-15": "Senior",
            "16-20": "Expert",
            "20+": "Veteran",
        }
        return experienceMap[experience as keyof typeof experienceMap] || experience
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
            <div className="max-w-7xl mx-auto space-y-6">
                {/* Header */}
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Teacher Applications</h1>
                        <p className="text-gray-600 mt-1">Manage and review teacher applications</p>
                    </div>
                    <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-lg px-3 py-1">
                            {teachers.length} Total Applications
                        </Badge>
                    </div>
                </div>

                {/* Status Overview Cards */}
                <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
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
                            <CardTitle className="text-sm font-medium">Interview Scheduled</CardTitle>
                            <Calendar className="h-4 w-4 text-purple-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-purple-600">{statusCounts["interview-scheduled"] || 0}</div>
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
                            <CardTitle className="text-sm font-medium">Rejected</CardTitle>
                            <XCircle className="h-4 w-4 text-red-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold text-red-600">{statusCounts.rejected || 0}</div>
                        </CardContent>
                    </Card>
                </div>

                {/* Teachers Table */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Users className="h-5 w-5" />
                            Teacher Applications
                        </CardTitle>
                        <CardDescription>Review and manage all teacher applications in one place</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="rounded-md border">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead className="w-[250px]">Applicant</TableHead>
                                        <TableHead>Position</TableHead>
                                        <TableHead>Experience</TableHead>
                                        <TableHead>Education</TableHead>
                                        <TableHead>Subjects</TableHead>
                                        <TableHead>Status</TableHead>
                                        <TableHead>Applied</TableHead>
                                        <TableHead>Flags</TableHead>
                                        <TableHead className="text-right">Actions</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {teachers.map((teacher) => (
                                        <TableRow key={teacher.id} className="hover:bg-gray-50">
                                            <TableCell>
                                                <div className="flex items-center gap-3">
                                                    <Avatar className="h-10 w-10">
                                                        <AvatarImage src={teacher.profilePhoto || "/placeholder.svg"} />
                                                        <AvatarFallback>{getInitials(teacher.firstName, teacher.lastName)}</AvatarFallback>
                                                    </Avatar>
                                                    <div>
                                                        <div className="font-medium">
                                                            {teacher.firstName} {teacher.lastName}
                                                        </div>
                                                        <div className="text-sm text-gray-500 flex items-center gap-1">
                                                            <Mail className="h-3 w-3" />
                                                            {teacher.personalEmail}
                                                        </div>
                                                        <div className="text-sm text-gray-500 flex items-center gap-1">
                                                            <Phone className="h-3 w-3" />
                                                            {teacher.primaryPhone}
                                                        </div>
                                                    </div>
                                                </div>
                                            </TableCell>

                                            <TableCell>
                                                <div>
                                                    <div className="font-medium">{teacher.positionApplyingFor}</div>
                                                    {teacher.departmentPreference && (
                                                        <div className="text-sm text-gray-500">{teacher.departmentPreference}</div>
                                                    )}
                                                    <div className="text-sm text-gray-500 flex items-center gap-1">
                                                        <MapPin className="h-3 w-3" />
                                                        {teacher.city}, {teacher.state}
                                                    </div>
                                                </div>
                                            </TableCell>

                                            <TableCell>
                                                <div>
                                                    <Badge variant="outline" className="mb-1">
                                                        {getExperienceLevel(teacher.yearsOfExperience)}
                                                    </Badge>
                                                    <div className="text-sm text-gray-500">{teacher.yearsOfExperience} years</div>
                                                    {teacher.teachingLicense && (
                                                        <div className="flex items-center gap-1 text-sm text-green-600">
                                                            <Award className="h-3 w-3" />
                                                            Licensed
                                                        </div>
                                                    )}
                                                </div>
                                            </TableCell>

                                            <TableCell>
                                                <div>
                                                    <div className="flex items-center gap-1">
                                                        <GraduationCap className="h-4 w-4 text-gray-500" />
                                                        <span className="capitalize text-sm font-medium">
                                                            {teacher.highestDegree.replace("-", " ")}
                                                        </span>
                                                    </div>
                                                    <div className="text-sm text-gray-500">{teacher.majorSubject}</div>
                                                    <div className="text-sm text-gray-500">{teacher.university}</div>
                                                    {teacher.gpa && <div className="text-sm text-gray-500">GPA: {teacher.gpa}</div>}
                                                </div>
                                            </TableCell>

                                            <TableCell>
                                                <div className="space-y-1">
                                                    <div className="flex flex-wrap gap-1">
                                                        {teacher.subjectsToTeach.slice(0, 2).map((subject) => (
                                                            <Badge key={subject} variant="secondary" className="text-xs">
                                                                {subject}
                                                            </Badge>
                                                        ))}
                                                        {teacher.subjectsToTeach.length > 2 && (
                                                            <Badge variant="outline" className="text-xs">
                                                                +{teacher.subjectsToTeach.length - 2}
                                                            </Badge>
                                                        )}
                                                    </div>
                                                    <div className="text-xs text-gray-500">
                                                        Grades: {teacher.gradeLevelsToTeach.slice(0, 3).join(", ")}
                                                        {teacher.gradeLevelsToTeach.length > 3 && "..."}
                                                    </div>
                                                </div>
                                            </TableCell>

                                            <TableCell>
                                                <TeacherStatusBadge status={teacher.status} />
                                            </TableCell>

                                            <TableCell>
                                                <div className="text-sm">{formatDate(teacher.applicationDate)}</div>
                                                <div className="text-xs text-gray-500">Available: {formatDate(teacher.availableStartDate)}</div>
                                            </TableCell>

                                            <TableCell>
                                                <div className="flex flex-col gap-1">
                                                    {teacher.hasConvictions && (
                                                        <Badge variant="destructive" className="text-xs flex items-center gap-1">
                                                            <AlertTriangle className="h-3 w-3" />
                                                            Criminal Record
                                                        </Badge>
                                                    )}
                                                    {teacher.hasDisciplinaryActions && (
                                                        <Badge variant="destructive" className="text-xs flex items-center gap-1">
                                                            <AlertTriangle className="h-3 w-3" />
                                                            Disciplinary
                                                        </Badge>
                                                    )}
                                                    {!teacher.teachingLicense && (
                                                        <Badge variant="secondary" className="text-xs">
                                                            No License
                                                        </Badge>
                                                    )}
                                                    {!teacher.hasConvictions && !teacher.hasDisciplinaryActions && teacher.teachingLicense && (
                                                        <Badge className="bg-green-100 text-green-800 text-xs flex items-center gap-1">
                                                            <CheckCircle className="h-3 w-3" />
                                                            Clean
                                                        </Badge>
                                                    )}
                                                </div>
                                            </TableCell>

                                            <TableCell className="text-right">
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => handleViewDetails(teacher)}
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

                {/* Teacher Detail Dialog */}
                <TeacherDetailDialog
                    teacher={selectedTeacher}
                    isOpen={isDetailDialogOpen}
                    onClose={() => {
                        setIsDetailDialogOpen(false)
                        setSelectedTeacher(null)
                    }}
                    onStatusChange={handleStatusChange}
                />
            </div>
        </div>
    )
}
