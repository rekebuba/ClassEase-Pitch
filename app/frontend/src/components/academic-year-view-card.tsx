import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Calendar, GraduationCap, BookOpen, Edit, Eye, Play, Archive, Copy } from "lucide-react"
import type { AcademicYear } from "@/lib/academic-year"
import { AcademicYearStatusBadge } from "@/components"

interface AcademicYearViewCardProps {
    academicYear: AcademicYear
    onEdit: () => void
    onView: () => void
    onActivate?: () => void
    onArchive?: () => void
    onDuplicate?: () => void
}

export default function AcademicYearViewCard({
    academicYear,
    onEdit,
    onView,
    onActivate,
    onArchive,
    onDuplicate,
}: AcademicYearViewCardProps) {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            year: "numeric",
            month: "short",
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

    const getTotalSubjectsInGrades = () => {
        return academicYear.grades.reduce((total, grade) => {
            if (grade.hasStreams) {
                return total + grade.streams.reduce((streamTotal, stream) => streamTotal + stream.subjects.length, 0)
            }
            return total + grade.subjects.length
        }, 0)
    }

    const getTotalStreams = () => {
        return academicYear.grades.reduce((total, grade) => total + grade.streams.length, 0)
    }

    const getTotalSections = () => {
        return academicYear.grades.reduce((total, grade) => total + grade.sections.length, 0)
    }

    return (
        <Card className="w-full hover:shadow-md transition-shadow">
            <CardHeader className="pb-4">
                <div className="flex items-start justify-between">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            <CardTitle className="text-lg">{academicYear.name}</CardTitle>
                            <AcademicYearStatusBadge status={academicYear.status} />
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-1">
                                <Calendar className="h-4 w-4" />
                                <span>
                                    {formatDate(academicYear.startDate)} - {formatDate(academicYear.endDate)}
                                </span>
                            </div>
                            <div className="flex items-center gap-1">
                                <span>•</span>
                                <span>{getDuration()}</span>
                            </div>
                            <div className="flex items-center gap-1">
                                <span>•</span>
                                <span className="capitalize">{academicYear.termSystem}</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={onView}>
                            <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="outline" size="sm" onClick={onEdit}>
                            <Edit className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            </CardHeader>

            <CardContent className="space-y-4">
                {/* Quick Stats */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="text-center p-3 bg-blue-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <GraduationCap className="h-5 w-5 text-blue-600" />
                        </div>
                        <div className="text-2xl font-bold text-blue-600">{academicYear.grades.length}</div>
                        <div className="text-xs text-blue-600">Grades</div>
                    </div>
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <BookOpen className="h-5 w-5 text-green-600" />
                        </div>
                        <div className="text-2xl font-bold text-green-600">{academicYear.subjects.length}</div>
                        <div className="text-xs text-green-600">Subjects</div>
                    </div>
                    <div className="text-center p-3 bg-purple-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <div className="w-5 h-5 bg-purple-600 rounded flex items-center justify-center">
                                <span className="text-white text-xs font-bold">S</span>
                            </div>
                        </div>
                        <div className="text-2xl font-bold text-purple-600">{getTotalStreams()}</div>
                        <div className="text-xs text-purple-600">Streams</div>
                    </div>
                    <div className="text-center p-3 bg-orange-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <div className="w-5 h-5 bg-orange-600 rounded flex items-center justify-center">
                                <span className="text-white text-xs font-bold">C</span>
                            </div>
                        </div>
                        <div className="text-2xl font-bold text-orange-600">{getTotalSections()}</div>
                        <div className="text-xs text-orange-600">Sections</div>
                    </div>
                </div>

                <Separator />

                {/* Grades Overview */}
                <div>
                    <h4 className="font-medium mb-3 text-sm">Grade Levels</h4>
                    <div className="flex flex-wrap gap-2">
                        {academicYear.grades.map((grade) => (
                            <div key={grade.id} className="flex items-center gap-1">
                                <Badge variant="outline" className="text-xs">
                                    {grade.name}
                                </Badge>
                                {grade.hasStreams && (
                                    <Badge variant="secondary" className="text-xs">
                                        {grade.streams.length} streams
                                    </Badge>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Subject Categories */}
                <div>
                    <h4 className="font-medium mb-3 text-sm">Subject Categories</h4>
                    <div className="flex flex-wrap gap-2">
                        {Array.from(new Set(academicYear.subjects.map((s) => s.category))).map((category) => {
                            const count = academicYear.subjects.filter((s) => s.category === category).length
                            return (
                                <Badge key={category} variant="outline" className="text-xs">
                                    {category} ({count})
                                </Badge>
                            )
                        })}
                    </div>
                </div>

                <Separator />

                {/* Action Buttons */}
                <div className="flex items-center justify-between">
                    <div className="text-xs text-gray-500">Last updated: {formatDate(academicYear.updatedAt)}</div>
                    <div className="flex items-center gap-2">
                        {onDuplicate && (
                            <Button variant="outline" size="sm" onClick={onDuplicate}>
                                <Copy className="h-4 w-4 mr-1" />
                                Duplicate
                            </Button>
                        )}
                        {academicYear.status === "draft" && onActivate && (
                            <Button variant="default" size="sm" onClick={onActivate}>
                                <Play className="h-4 w-4 mr-1" />
                                Activate
                            </Button>
                        )}
                        {academicYear.status === "active" && onArchive && (
                            <Button variant="outline" size="sm" onClick={onArchive}>
                                <Archive className="h-4 w-4 mr-1" />
                                Archive
                            </Button>
                        )}
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
