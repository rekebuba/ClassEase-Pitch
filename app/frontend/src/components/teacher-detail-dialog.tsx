"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
    User,
    MapPin,
    GraduationCap,
    Award,
    Briefcase,
    Shield,
    FileText,
    Phone,
    Mail,
    Calendar,
    Globe,
    Users,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Eye,
} from "lucide-react"
import type { TeacherApplicationWithDetails } from "@/lib/api-validation"
import { TeacherStatusBadge } from "@/components"
import { updateTeacherApplicationStatus } from "@/api"
import { toast } from "sonner"

interface TeacherDetailDialogProps {
    teacher: TeacherApplicationWithDetails | null
    isOpen: boolean
    onClose: () => void
    onStatusChange: (teacherId: string, newStatus: TeacherApplicationWithDetails["status"]) => void
}

export default function TeacherDetailDialog({ teacher, isOpen, onClose, onStatusChange }: TeacherDetailDialogProps) {
    const [isUpdating, setIsUpdating] = useState(false)

    if (!teacher) return null

    const handleStatusChange = async (newStatus: TeacherApplicationWithDetails["status"]) => {
        setIsUpdating(true)
        const response = await updateTeacherApplicationStatus(teacher.id, newStatus)
        toast.success(response.message, {
            style: { color: "green" },
        })
        onStatusChange(teacher.id, newStatus)
        setIsUpdating(false)
    }

    const getInitials = (firstName: string, lastName: string) => {
        return `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase()
    }

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        })
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

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="fixed top-10 right-[10%] max-w-6xl max-h-[90vh] overflow-hidden">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-3">
                        <Avatar className="h-10 w-10">
                            <AvatarImage src={teacher.profilePhoto || "/placeholder.svg"} />
                            <AvatarFallback>{getInitials(teacher.firstName, teacher.fatherName)}</AvatarFallback>
                        </Avatar>
                        <div>
                            <div className="flex items-center gap-2">
                                <span>
                                    {teacher.firstName} {teacher.fatherName} {teacher.grandFatherName}
                                </span>
                                <TeacherStatusBadge status={teacher.status} />
                            </div>
                            <p className="text-sm text-gray-500">{teacher.positionApplyingFor}</p>
                        </div>
                    </DialogTitle>
                </DialogHeader>

                <ScrollArea className="max-h-[calc(90vh-120px)]">
                    <div className="space-y-6">
                        {/* Quick Actions */}
                        <Card>
                            <CardHeader>
                                <CardTitle className="text-lg">Quick Actions</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="flex flex-wrap gap-2">
                                    <Button
                                        size="sm"
                                        variant={teacher.status === "under-review" ? "default" : "outline"}
                                        onClick={() => handleStatusChange("under-review")}
                                        disabled={isUpdating}
                                    >
                                        <Eye className="h-4 w-4 mr-1" />
                                        Review
                                    </Button>
                                    <Button
                                        size="sm"
                                        variant={teacher.status === "interview-scheduled" ? "default" : "outline"}
                                        onClick={() => handleStatusChange("interview-scheduled")}
                                        disabled={isUpdating}
                                    >
                                        <Calendar className="h-4 w-4 mr-1" />
                                        Schedule Interview
                                    </Button>
                                    <Button
                                        size="sm"
                                        variant={teacher.status === "approved" ? "default" : "outline"}
                                        onClick={() => handleStatusChange("approved")}
                                        disabled={isUpdating}
                                        className="bg-green-600 hover:bg-green-700 text-white"
                                    >
                                        <CheckCircle className="h-4 w-4 mr-1" />
                                        Approve
                                    </Button>
                                    <Button
                                        size="sm"
                                        variant={teacher.status === "rejected" ? "destructive" : "outline"}
                                        onClick={() => handleStatusChange("rejected")}
                                        disabled={isUpdating}
                                    >
                                        <XCircle className="h-4 w-4 mr-1" />
                                        Reject
                                    </Button>
                                </div>
                            </CardContent>
                        </Card>

                        <Tabs defaultValue="personal" className="w-full">
                            <TabsList className="grid w-full grid-cols-6">
                                <TabsTrigger value="personal">Personal</TabsTrigger>
                                <TabsTrigger value="education">Education</TabsTrigger>
                                <TabsTrigger value="experience">Experience</TabsTrigger>
                                <TabsTrigger value="skills">Skills</TabsTrigger>
                                <TabsTrigger value="background">Background</TabsTrigger>
                                <TabsTrigger value="documents">Documents</TabsTrigger>
                            </TabsList>

                            <TabsContent value="personal" className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <Card>
                                        <CardHeader>
                                            <CardTitle className="flex items-center gap-2">
                                                <User className="h-5 w-5" />
                                                Personal Information
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent className="space-y-3">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Full Name</p>
                                                <p>
                                                    {teacher.firstName} {teacher.fatherName} {teacher.grandFatherName}
                                                </p>
                                                {teacher.firstName && (
                                                    <p className="text-sm text-gray-600">Preferred: {teacher.firstName}</p>
                                                )}
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Date of Birth</p>
                                                <p>
                                                    {formatDate(teacher.dateOfBirth)} ({calculateAge(teacher.dateOfBirth)} years old)
                                                </p>
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Gender</p>
                                                <p className="capitalize">{teacher.gender.replace("-", " ")}</p>
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Nationality</p>
                                                <p>{teacher.nationality}</p>
                                            </div>
                                            {teacher.maritalStatus && (
                                                <div>
                                                    <p className="text-sm font-medium text-gray-500">Marital Status</p>
                                                    <p className="capitalize">{teacher.maritalStatus.replace("-", " ")}</p>
                                                </div>
                                            )}
                                        </CardContent>
                                    </Card>

                                    <Card>
                                        <CardHeader>
                                            <CardTitle className="flex items-center gap-2">
                                                <MapPin className="h-5 w-5" />
                                                Contact Information
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent className="space-y-3">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Address</p>
                                                <p>{teacher.address}</p>
                                                <p>
                                                    {teacher.city}, {teacher.state} {teacher.postalCode}
                                                </p>
                                                <p>{teacher.country}</p>
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                                                    <Phone className="h-4 w-4" />
                                                    Phone Numbers
                                                </p>
                                                <p>Primary: {teacher.primaryPhone}</p>
                                                {teacher.secondaryPhone && <p>Secondary: {teacher.secondaryPhone}</p>}
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500 flex items-center gap-1">
                                                    <Mail className="h-4 w-4" />
                                                    Email Addresses
                                                </p>
                                                <p>Personal: {teacher.personalEmail}</p>
                                            </div>
                                        </CardContent>
                                    </Card>
                                </div>

                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <Users className="h-5 w-5" />
                                            Emergency Contact
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Name</p>
                                                <p>{teacher.emergencyContactName}</p>
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Relationship</p>
                                                <p>{teacher.emergencyContactRelation}</p>
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Phone</p>
                                                <p>{teacher.emergencyContactPhone}</p>
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value="education" className="space-y-4">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <GraduationCap className="h-5 w-5" />
                                            Educational Background
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Highest Degree</p>
                                                <p className="capitalize">{teacher.highestDegree.replace("-", " ")}</p>
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">University</p>
                                                <p>{teacher.university}</p>
                                            </div>
                                        </div>
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Graduation Year</p>
                                                <p>{teacher.graduationYear}</p>
                                            </div>
                                        </div>
                                        {teacher.gpa && (
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">GPA</p>
                                                <p>{teacher.gpa}/4.0</p>
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value="experience" className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <Card>
                                        <CardHeader>
                                            <CardTitle className="flex items-center gap-2">
                                                <Award className="h-5 w-5" />
                                                Teaching Credentials
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent className="space-y-3">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Teaching License</p>
                                                <div className="flex items-center gap-2">
                                                    {teacher.teachingLicense ? (
                                                        <Badge className="bg-green-100 text-green-800">Licensed</Badge>
                                                    ) : (
                                                        <Badge variant="secondary">Not Licensed</Badge>
                                                    )}
                                                </div>
                                                {teacher.teachingLicense && (
                                                    <div className="mt-2 space-y-1">
                                                        <p className="text-sm">License #: {teacher.licenseNumber}</p>
                                                        <p className="text-sm">State: {teacher.licenseState}</p>
                                                        <p className="text-sm">
                                                            Expires: {teacher.licenseExpirationDate && formatDate(teacher.licenseExpirationDate)}
                                                        </p>
                                                    </div>
                                                )}
                                            </div>
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Years of Experience</p>
                                                <p>{teacher.yearsOfExperience} years</p>
                                            </div>
                                            {teacher.preferredSchedule && (
                                                <div>
                                                    <p className="text-sm font-medium text-gray-500">Preferred Schedule</p>
                                                    <p className="capitalize">{teacher.preferredSchedule.replace("-", " ")}</p>
                                                </div>
                                            )}
                                        </CardContent>
                                    </Card>

                                    <Card>
                                        <CardHeader>
                                            <CardTitle className="flex items-center gap-2">
                                                <Briefcase className="h-5 w-5" />
                                                Position Details
                                            </CardTitle>
                                        </CardHeader>
                                        <CardContent className="space-y-3">
                                            <div>
                                                <p className="text-sm font-medium text-gray-500">Position Applying For</p>
                                                <p>{teacher.positionApplyingFor}</p>
                                            </div>
                                            {teacher.salaryExpectation && (
                                                <div>
                                                    <p className="text-sm font-medium text-gray-500">Salary Expectation</p>
                                                    <p>{teacher.salaryExpectation}</p>
                                                </div>
                                            )}
                                        </CardContent>
                                    </Card>
                                </div>

                                <Card>
                                    <CardHeader>
                                        <CardTitle>Teaching Subjects & Grade Levels</CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div>
                                            <p className="text-sm font-medium text-gray-500 mb-2">Subjects to Teach</p>
                                            <div className="flex flex-wrap gap-1">
                                                {teacher.subjectsToTeach.map((subject) => (
                                                    <Badge key={subject} variant="secondary">
                                                        {subject}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                        <div>
                                            <p className="text-sm font-medium text-gray-500 mb-2">Grade Levels</p>
                                            <div className="flex flex-wrap gap-1">
                                                {teacher.gradeLevelsToTeach.map((grade) => (
                                                    <Badge key={grade} variant="outline">
                                                        Grade {grade}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>

                                {teacher.previousSchools && (
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Previous Experience</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="whitespace-pre-wrap">{teacher.previousSchools}</p>
                                        </CardContent>
                                    </Card>
                                )}
                            </TabsContent>

                            <TabsContent value="skills" className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <Card>
                                        <CardHeader>
                                            <CardTitle className="flex items-center gap-2">
                                                <Globe className="h-5 w-5" />
                                                Languages & Technology
                                            </CardTitle>
                                        </CardHeader>
                                    </Card>

                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Certifications & Specializations</CardTitle>
                                        </CardHeader>
                                    </Card>
                                </div>

                                {teacher.specialSkills && (
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Special Skills & Abilities</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="whitespace-pre-wrap">{teacher.specialSkills}</p>
                                        </CardContent>
                                    </Card>
                                )}

                                {teacher.teachingPhilosophy && (
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Teaching Philosophy</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="whitespace-pre-wrap">{teacher.teachingPhilosophy}</p>
                                        </CardContent>
                                    </Card>
                                )}

                                {teacher.whyTeaching && (
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Why Teaching?</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="whitespace-pre-wrap">{teacher.whyTeaching}</p>
                                        </CardContent>
                                    </Card>
                                )}
                            </TabsContent>

                            <TabsContent value="background" className="space-y-4">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <Shield className="h-5 w-5" />
                                            Background Information
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div className="flex items-center gap-2">
                                                <p className="text-sm font-medium text-gray-500">Criminal Convictions:</p>
                                                {teacher.hasConvictions ? (
                                                    <Badge variant="destructive" className="flex items-center gap-1">
                                                        <AlertTriangle className="h-3 w-3" />
                                                        Yes
                                                    </Badge>
                                                ) : (
                                                    <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                                                        <CheckCircle className="h-3 w-3" />
                                                        No
                                                    </Badge>
                                                )}
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <p className="text-sm font-medium text-gray-500">Disciplinary Actions:</p>
                                                {teacher.hasDisciplinaryActions ? (
                                                    <Badge variant="destructive" className="flex items-center gap-1">
                                                        <AlertTriangle className="h-3 w-3" />
                                                        Yes
                                                    </Badge>
                                                ) : (
                                                    <Badge className="bg-green-100 text-green-800 flex items-center gap-1">
                                                        <CheckCircle className="h-3 w-3" />
                                                        No
                                                    </Badge>
                                                )}
                                            </div>
                                        </div>

                                        {teacher.convictionDetails && (
                                            <div className="p-4 bg-red-50 rounded-lg">
                                                <p className="text-sm font-medium text-red-800 mb-2">Conviction Details:</p>
                                                <p className="text-sm text-red-700">{teacher.convictionDetails}</p>
                                            </div>
                                        )}

                                        {teacher.disciplinaryDetails && (
                                            <div className="p-4 bg-orange-50 rounded-lg">
                                                <p className="text-sm font-medium text-orange-800 mb-2">Disciplinary Action Details:</p>
                                                <p className="text-sm text-orange-700">{teacher.disciplinaryDetails}</p>
                                            </div>
                                        )}
                                    </CardContent>
                                </Card>

                                <Card>
                                    <CardHeader>
                                        <CardTitle>Professional References</CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                            <div className="p-4 border rounded-lg">
                                                <h4 className="font-medium mb-2">Reference 1</h4>
                                                <div className="space-y-1 text-sm">
                                                    <p>
                                                        <strong>{teacher.reference1Name}</strong>
                                                    </p>
                                                    <p>{teacher.reference1Title}</p>
                                                    <p>{teacher.reference1Organization}</p>
                                                    <p>{teacher.reference1Phone}</p>
                                                    <p>{teacher.reference1Email}</p>
                                                </div>
                                            </div>

                                            {teacher.reference2Name && (
                                                <div className="p-4 border rounded-lg">
                                                    <h4 className="font-medium mb-2">Reference 2</h4>
                                                    <div className="space-y-1 text-sm">
                                                        <p>
                                                            <strong>{teacher.reference2Name}</strong>
                                                        </p>
                                                        <p>{teacher.reference2Title}</p>
                                                        <p>{teacher.reference2Organization}</p>
                                                        <p>{teacher.reference2Phone}</p>
                                                        <p>{teacher.reference2Email}</p>
                                                    </div>
                                                </div>
                                            )}

                                            {teacher.reference3Name && (
                                                <div className="p-4 border rounded-lg">
                                                    <h4 className="font-medium mb-2">Reference 3</h4>
                                                    <div className="space-y-1 text-sm">
                                                        <p>
                                                            <strong>{teacher.reference3Name}</strong>
                                                        </p>
                                                        <p>{teacher.reference3Title}</p>
                                                        <p>{teacher.reference3Organization}</p>
                                                        <p>{teacher.reference3Phone}</p>
                                                        <p>{teacher.reference3Email}</p>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            <TabsContent value="documents" className="space-y-4">
                                <Card>
                                    <CardHeader>
                                        <CardTitle className="flex items-center gap-2">
                                            <FileText className="h-5 w-5" />
                                            Submitted Documents
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            {[
                                                { label: "Resume/CV", file: teacher.resume, required: true },
                                                { label: "Cover Letter", file: teacher.coverLetter, required: false },
                                                { label: "Transcripts", file: teacher.transcripts, required: false },
                                                { label: "Teaching Certificate", file: teacher.teachingCertificate, required: false },
                                                { label: "Background Check", file: teacher.backgroundCheck, required: false },
                                            ].map((doc) => (
                                                <div key={doc.label} className="flex items-center justify-between p-3 border rounded-lg">
                                                    <div className="flex items-center gap-2">
                                                        <FileText className="h-4 w-4 text-gray-500" />
                                                        <span className="text-sm font-medium">{doc.label}</span>
                                                        {doc.required && (
                                                            <Badge variant="outline" className="text-xs">
                                                                Required
                                                            </Badge>
                                                        )}
                                                    </div>
                                                    {doc.file ? (
                                                        <Badge className="bg-green-100 text-green-800">
                                                            <CheckCircle className="h-3 w-3 mr-1" />
                                                            Uploaded
                                                        </Badge>
                                                    ) : (
                                                        <Badge variant="secondary">
                                                            <XCircle className="h-3 w-3 mr-1" />
                                                            Missing
                                                        </Badge>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </CardContent>
                                </Card>

                                {teacher.additionalComments && (
                                    <Card>
                                        <CardHeader>
                                            <CardTitle>Additional Comments</CardTitle>
                                        </CardHeader>
                                        <CardContent>
                                            <p className="whitespace-pre-wrap">{teacher.additionalComments}</p>
                                        </CardContent>
                                    </Card>
                                )}
                            </TabsContent>
                        </Tabs>
                    </div>
                </ScrollArea>
            </DialogContent>
        </Dialog>
    )
}
