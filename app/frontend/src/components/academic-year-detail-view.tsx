import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Calendar, GraduationCap, BookOpen, Users, Layers, ArrowLeft, Edit } from "lucide-react"
import type { AcademicYear } from "@/lib/academic-year"
import { AcademicYearStatusBadge } from "@/components"

interface AcademicYearDetailViewProps {
    academicYear: AcademicYear
    onBack: () => void
    onEdit: () => void
}

export default function AcademicYearDetailView({ academicYear, onBack, onEdit }: AcademicYearDetailViewProps) {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        })
    }

    const getDuration = () => {
        const start = new Date(academicYear.startDate)
        const end = new Date(academicYear.endDate)
        const diffTime = Math.abs(end.getTime() - start.getTime())
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
        return `${diffDays} days`
    }

    const getCategoryColor = (category: string) => {
        const colors = {
            core: "bg-blue-100 text-blue-800",
            elective: "bg-green-100 text-green-800",
            language: "bg-purple-100 text-purple-800",
            arts: "bg-pink-100 text-pink-800",
            physical: "bg-orange-100 text-orange-800",
            technical: "bg-gray-100 text-gray-800",
        }
        return colors[category as keyof typeof colors] || colors.core
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Button variant="outline" size="sm" onClick={onBack}>
                        <ArrowLeft className="h-4 w-4 mr-2" />
                        Back
                    </Button>
                    <div>
                        <h1 className="text-2xl font-bold">{academicYear.name}</h1>
                        <div className="flex items-center gap-3 mt-1">
                            <AcademicYearStatusBadge status={academicYear.status} />
                            <span className="text-sm text-gray-600">
                                {formatDate(academicYear.startDate)} - {formatDate(academicYear.endDate)}
                            </span>
                        </div>
                    </div>
                </div>
                <Button onClick={onEdit}>
                    <Edit className="h-4 w-4 mr-2" />
                    Edit Configuration
                </Button>
            </div>

            {/* Basic Information */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Calendar className="h-5 w-5" />
                        Basic Information
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Academic Year</h4>
                            <p className="font-medium">{academicYear.name}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Duration</h4>
                            <p className="font-medium">{getDuration()}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Term System</h4>
                            <p className="font-medium capitalize">{academicYear.termSystem}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Start Date</h4>
                            <p className="font-medium">{formatDate(academicYear.startDate)}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">End Date</h4>
                            <p className="font-medium">{formatDate(academicYear.endDate)}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Status</h4>
                            <AcademicYearStatusBadge status={academicYear.status} />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Grades and Streams */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <GraduationCap className="h-5 w-5" />
                        Grades & Academic Streams ({academicYear.grades.length})
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {academicYear.grades.map((grade) => (
                            <Card key={grade.id} className="border-l-4 border-l-blue-500">
                                <CardContent className="p-4">
                                    <div className="flex items-start justify-between mb-3">
                                        <div>
                                            <h4 className="font-medium text-lg">{grade.name}</h4>
                                            <p className="text-sm text-gray-600">Level {grade.level}</p>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Badge variant="outline" className="flex items-center gap-1">
                                                <Users className="h-3 w-3" />
                                                {grade.sections.length} Sections
                                            </Badge>
                                            {grade.hasStreams && (
                                                <Badge variant="secondary" className="flex items-center gap-1">
                                                    <Layers className="h-3 w-3" />
                                                    {grade.streams.length} Streams
                                                </Badge>
                                            )}
                                        </div>
                                    </div>

                                    {/* Sections */}
                                    <div className="mb-3">
                                        <h5 className="font-medium text-sm mb-2">Sections:</h5>
                                        <div className="flex flex-wrap gap-1">
                                            {grade.sections.map((section) => (
                                                <Badge key={section} variant="outline" className="text-xs">
                                                    Section {section}
                                                </Badge>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Streams */}
                                    {grade.hasStreams && grade.streams.length > 0 && (
                                        <div className="mb-3">
                                            <h5 className="font-medium text-sm mb-2">Academic Streams:</h5>
                                            <div className="space-y-2">
                                                {grade.streams.map((stream) => (
                                                    <div key={stream.id} className="bg-gray-50 p-3 rounded-lg">
                                                        <div className="flex items-center justify-between mb-2">
                                                            <div>
                                                                <h6 className="font-medium">{stream.name}</h6>
                                                                <p className="text-sm text-gray-600">{stream.description}</p>
                                                            </div>
                                                            <Badge variant="outline">{stream.code}</Badge>
                                                        </div>
                                                        <div>
                                                            <span className="text-sm font-medium">Subjects: </span>
                                                            <div className="flex flex-wrap gap-1 mt-1">
                                                                {stream.subjects.map((subject) => (
                                                                    <Badge key={subject} variant="secondary" className="text-xs">
                                                                        {subject}
                                                                    </Badge>
                                                                ))}
                                                            </div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Grade Subjects (for non-stream grades) */}
                                    {!grade.hasStreams && (
                                        <div>
                                            <h5 className="font-medium text-sm mb-2">Subjects:</h5>
                                            <div className="flex flex-wrap gap-1">
                                                {grade.subjects.map((subject) => (
                                                    <Badge key={subject} variant="secondary" className="text-xs">
                                                        {subject}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Subjects */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        Subjects ({academicYear.subjects.length})
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {/* Subject Categories */}
                        {Array.from(new Set(academicYear.subjects.map((s) => s.category))).map((category) => {
                            const categorySubjects = academicYear.subjects.filter((s) => s.category === category)
                            return (
                                <div key={category}>
                                    <h4 className="font-medium mb-3 capitalize flex items-center gap-2">
                                        <Badge className={getCategoryColor(category)}>{category}</Badge>
                                        <span>({categorySubjects.length} subjects)</span>
                                    </h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                                        {categorySubjects.map((subject) => (
                                            <Card key={subject.id} className="p-3">
                                                <div className="flex items-start justify-between">
                                                    <div className="flex-1">
                                                        <div className="flex items-center gap-2 mb-1">
                                                            <h5 className="font-medium text-sm">{subject.name}</h5>
                                                            <Badge variant="outline" className="text-xs">
                                                                {subject.code}
                                                            </Badge>
                                                        </div>
                                                        <p className="text-xs text-gray-600 mb-2">{subject.description}</p>
                                                        {subject.isRequired && (
                                                            <Badge variant="destructive" className="text-xs">
                                                                Required
                                                            </Badge>
                                                        )}
                                                    </div>
                                                </div>
                                            </Card>
                                        ))}
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </CardContent>
            </Card>

            {/* Metadata */}
            <Card>
                <CardHeader>
                    <CardTitle>Configuration History</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-gray-600">Created:</span>
                            <div className="font-medium">{formatDate(academicYear.createdAt)}</div>
                        </div>
                        <div>
                            <span className="text-gray-600">Last Updated:</span>
                            <div className="font-medium">{formatDate(academicYear.updatedAt)}</div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
