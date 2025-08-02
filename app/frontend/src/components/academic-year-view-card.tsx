import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Calendar, GraduationCap, BookOpen, Edit, Eye, Play, Archive, Copy } from "lucide-react"
// import type { AcademicYear } from "@/lib/academic-year"
import { AcademicYearStatusBadge } from "@/components"
import { useEffect, useState } from "react"
import type { AcademicTerm, Grade, Subject, Year, Event } from "@/lib/api-response-type"
import { pickFields } from "@/utils/pick-zod-fields"
import { AcademicTermSchema, EventSchema, GradeSchema, SubjectSchema, YearSchema } from "@/lib/api-response-validation"
import { AcademicYear } from "@/pages/admin/academic-year-management"
import { sharedApi } from "@/api"
import { z } from "zod"
import { toast } from "sonner"
import { Skeleton } from "@/components/ui/skeleton"

interface AcademicYearViewCardProps {
    academicYear: AcademicYear
    onEdit: (detailAcademicYear: DetailAcademicYear) => void
    onView: (detailAcademicYear: DetailAcademicYear) => void
    onActivate?: (detailAcademicYear: DetailAcademicYear) => void
    onArchive?: (detailAcademicYear: DetailAcademicYear) => void
    onDuplicate?: (detailAcademicYear: DetailAcademicYear) => void
}

export type DetailAcademicYear = Pick<Year, "id" | "calendarType" | "name" | "startDate" | "endDate" | "status" | "createdAt" | "updatedAt"> & {
    grades: Pick<Grade, "id" | "grade" | "level" | "hasStream">[]
    subjects: Pick<Subject, "id" | "name" | "code">[]
    academicTerms: Pick<AcademicTerm, "id" | "name">[]
    events: Pick<Event, "id" | "title">[]
}

export default function AcademicYearViewCard({
    academicYear,
    onEdit,
    onView,
    onActivate,
    onArchive,
    onDuplicate,
}: AcademicYearViewCardProps) {
    const [detailAcademicYears, setDetailAcademicYears] = useState<DetailAcademicYear | null>(null)
    
    useEffect(() => {
        const fetchAcademicYear = async () => {
            const gradeFields = [
                "id",
                "grade",
                "level",
                "hasStream",
            ] as const
            const subjectFields = [
                "id",
                "name",
                "code",
            ] as const
            const academicTermFields = [
                "id",
                "name",
            ] as const
            const eventFields = [
                "id",
                "title",
            ] as const
            const selectedSchema = z.object({
                grades: z.array(pickFields(GradeSchema, gradeFields)),
                subjects: z.array(pickFields(SubjectSchema, subjectFields)),
                academicTerms: z.array(pickFields(AcademicTermSchema, academicTermFields)),
                events: z.array(pickFields(EventSchema, eventFields)),
            });

            const response = await sharedApi.getYearDetail(academicYear.id, selectedSchema, {
                expand: ["grades", "subjects", "academicTerms", "events"],
                nestedFields: { "grades": [...gradeFields], "subjects": [...subjectFields], "academicTerms": [...academicTermFields], "events": [...eventFields] },
            });

            if (!response.success) {
                toast.error(response.error.message, {
                    style: { color: "red" },
                });
                return;
            }

            setDetailAcademicYears({ ...academicYear, ...response.data });
        };

        fetchAcademicYear();
    }, []);

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

    // const getTotalSubjectsInGrades = () => {
    //     return detailAcademicYears.grades.reduce((total, grade) => {
    //         if (grade.hasStreams) {
    //             return total + grade.streams.reduce((streamTotal, stream) => streamTotal + stream.subjects.length, 0)
    //         }
    //         return total + grade.subjects.length
    //     }, 0)
    // }

    const getTotalSections = () => {
        return 0
    }

    if (!detailAcademicYears) {
        return (
            <Card className="w-full hover:shadow-md transition-shadow">
                <CardHeader className="pb-4">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                                <Skeleton className="h-5 w-32 rounded" />
                                <Skeleton className="h-5 w-20 rounded" />
                            </div>
                            <div className="flex items-center gap-4 text-sm text-gray-600">
                                <Skeleton className="h-4 w-52" />
                                <Skeleton className="h-4 w-12" />
                                <Skeleton className="h-4 w-20" />
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <Skeleton className="h-8 w-8 rounded" />
                            <Skeleton className="h-8 w-8 rounded" />
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="space-y-4">
                    {/* Quick Stats */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {[...Array(4)].map((_, i) => (
                            <div key={i} className="text-center p-3 rounded-lg bg-muted">
                                <Skeleton className="h-5 w-5 mx-auto mb-2 rounded-full" />
                                <Skeleton className="h-6 w-10 mx-auto rounded" />
                                <Skeleton className="h-3 w-16 mx-auto mt-1 rounded" />
                            </div>
                        ))}
                    </div>

                    <Separator />

                    {/* Grade Levels */}
                    <div>
                        <Skeleton className="h-4 w-28 mb-3 rounded" />
                        <div className="flex flex-wrap gap-2">
                            {[...Array(6)].map((_, i) => (
                                <Skeleton key={i} className="h-5 w-16 rounded" />
                            ))}
                        </div>
                    </div>

                    {/* Subjects */}
                    <div>
                        <Skeleton className="h-4 w-20 mb-3 rounded" />
                        <div className="flex flex-wrap gap-2">
                            {[...Array(5)].map((_, i) => (
                                <Skeleton key={i} className="h-5 w-24 rounded" />
                            ))}
                        </div>
                    </div>

                    <Separator />

                    {/* Footer Actions */}
                    <div className="flex items-center justify-between">
                        <Skeleton className="h-4 w-32 rounded" />
                        <div className="flex items-center gap-2">
                            <Skeleton className="h-8 w-24 rounded" />
                            <Skeleton className="h-8 w-24 rounded" />
                            <Skeleton className="h-8 w-24 rounded" />
                        </div>
                    </div>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="w-full hover:shadow-md transition-shadow">
            <CardHeader className="pb-4">
                <div className="flex items-start justify-between">
                    <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                            <CardTitle className="text-lg">{detailAcademicYears.name}</CardTitle>
                            <AcademicYearStatusBadge status={detailAcademicYears.status} />
                        </div>
                        <div className="flex items-center gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-1">
                                <Calendar className="h-4 w-4" />
                                <span>
                                    {formatDate(detailAcademicYears.startDate)} - {formatDate(detailAcademicYears.endDate)}
                                </span>
                            </div>
                            <div className="flex items-center gap-1">
                                <span>•</span>
                                <span>{getDuration()}</span>
                            </div>
                            <div className="flex items-center gap-1">
                                <span>•</span>
                                <span className="capitalize">{detailAcademicYears.calendarType}</span>
                            </div>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={() => onView(detailAcademicYears)}>
                            <Eye className="h-4 w-4" />
                        </Button>
                        <Button variant="outline" size="sm" onClick={() => onEdit(detailAcademicYears)}>
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
                        <div className="text-2xl font-bold text-blue-600">{detailAcademicYears.grades.length}</div>
                        <div className="text-xs text-blue-600">Grades</div>
                    </div>
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <BookOpen className="h-5 w-5 text-green-600" />
                        </div>
                        <div className="text-2xl font-bold text-green-600">{detailAcademicYears.subjects.length}</div>
                        <div className="text-xs text-green-600">Subjects</div>
                    </div>
                    <div className="text-center p-3 bg-purple-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <div className="w-5 h-5 bg-purple-600 rounded flex items-center justify-center">
                                <span className="text-white text-xs font-bold">T</span>
                            </div>
                        </div>
                        <div className="text-2xl font-bold text-purple-600">{detailAcademicYears.academicTerms.length}</div>
                        <div className="text-xs text-purple-600">Terms</div>
                    </div>
                    <div className="text-center p-3 bg-orange-50 rounded-lg">
                        <div className="flex items-center justify-center mb-1">
                            <div className="w-5 h-5 bg-orange-600 rounded flex items-center justify-center">
                                <span className="text-white text-xs font-bold">E</span>
                            </div>
                        </div>
                        <div className="text-2xl font-bold text-orange-600">{detailAcademicYears.events.length}</div>
                        <div className="text-xs text-orange-600">Events</div>
                    </div>
                </div>

                <Separator />

                {/* Grades Overview */}
                <div>
                    <h4 className="font-medium mb-3 text-sm">Grade Levels</h4>
                    <div className="flex flex-wrap gap-2">
                        {[...detailAcademicYears.grades]
                            .sort((a, b) => Number(a.grade) - Number(b.grade))
                            .map((grade) => (
                                <div key={grade.id} className="flex items-center gap-1">
                                    <Badge variant="secondary" className="text-xs">
                                        Grade {grade.grade}
                                    </Badge>
                                </div>
                            ))}
                    </div>
                </div>

                {/* Subject Categories */}
                <div>
                    <h4 className="font-medium mb-3 text-sm">Subject</h4>
                    <div className="flex flex-wrap gap-2">
                        {detailAcademicYears.subjects.map((subjects) => (
                            <div key={subjects.id} className="flex items-center gap-1">
                                <Badge variant="secondary" className="text-xs">
                                    {subjects.name}
                                </Badge>
                            </div>
                        ))}
                    </div>
                </div>
                <Separator />

                {/* Action Buttons */}
                <div className="flex items-center justify-between">
                    <div className="text-xs text-gray-500">Last updated: {formatDate(detailAcademicYears.updatedAt)}</div>
                    <div className="flex items-center gap-2">
                        {onDuplicate && (
                            <Button variant="outline" size="sm" onClick={() => onDuplicate(detailAcademicYears)}>
                                <Copy className="h-4 w-4 mr-1" />
                                Duplicate
                            </Button>
                        )}
                        {detailAcademicYears.status === "draft" && onActivate && (
                            <Button variant="default" size="sm" onClick={() => onActivate(detailAcademicYears)}>
                                <Play className="h-4 w-4 mr-1" />
                                Activate
                            </Button>
                        )}
                        {detailAcademicYears.status === "active" && onArchive && (
                            <Button variant="outline" size="sm" onClick={() => onArchive(detailAcademicYears)}>
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
