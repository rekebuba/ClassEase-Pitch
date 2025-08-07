import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Calendar, GraduationCap, BookOpen, Trash2, MoreHorizontal, Eye, Users, Layers, ArrowLeft, Edit } from "lucide-react"
import type { AcademicYear } from "@/pages/admin/academic-year-management"
import { AcademicYearStatusBadge } from "@/components"
import { z } from "zod"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { AcademicTermSchema, EventSchema, GradeSchema, SectionSchema, StreamSchema, SubjectSchema } from "@/lib/api-response-validation"
import { pickFields } from "@/utils/pick-zod-fields"
import { sharedApi } from "@/api"
import { toast } from "sonner"
import { useEffect, useRef, useState } from "react"
import { DetailAcademicYear } from "./academic-year-view-card"
import { Grade, Section, Stream, Subject } from "@/lib/api-response-type"
import { Skeleton } from "./ui/skeleton"
import FadeIn from "./fade-in"
import { useQueries } from "@tanstack/react-query"

interface AcademicYearDetailViewProps {
    detailAcademicYears: DetailAcademicYear
    onBack: () => void
    onEdit: () => void
}

type DetailGrade = Pick<Grade, "id" | "grade" | "level" | "hasStream"> & {
    sections: Pick<Section, "id" | "section">[]
    streams: Pick<Stream, "id" | "name">[],
    subjects: Pick<Subject, "id" | "name" | "code">[]
}

type DetailSubject = Pick<Subject, "id" | "name" | "code"> & {
    streams: Pick<Stream, "id" | "name">[]
    grades: Pick<Grade, "id" | "grade">[]
}

export default function AcademicYearDetailView({ detailAcademicYears, onBack, onEdit }: AcademicYearDetailViewProps) {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString("en-US", {
            year: "numeric",
            month: "long",
            day: "numeric",
        })
    }

    const getDuration = () => {
        const start = new Date(detailAcademicYears.startDate)
        const end = new Date(detailAcademicYears.endDate)
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
                        <h1 className="text-2xl font-bold">{detailAcademicYears.name}</h1>
                        <div className="flex items-center gap-3 mt-1">
                            <AcademicYearStatusBadge status={detailAcademicYears.status} />
                            <span className="text-sm text-gray-600">
                                {formatDate(detailAcademicYears.startDate)} - {formatDate(detailAcademicYears.endDate)}
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
                            <p className="font-medium">{detailAcademicYears.name}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Duration</h4>
                            <p className="font-medium">{getDuration()}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Term System</h4>
                            <p className="font-medium capitalize">{detailAcademicYears.calendarType}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Start Date</h4>
                            <p className="font-medium">{formatDate(detailAcademicYears.startDate)}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">End Date</h4>
                            <p className="font-medium">{formatDate(detailAcademicYears.endDate)}</p>
                        </div>
                        <div>
                            <h4 className="font-medium text-sm text-gray-600 mb-1">Status</h4>
                            <AcademicYearStatusBadge status={detailAcademicYears.status} />
                        </div>
                    </div>
                </CardContent>
            </Card>


            <Tabs defaultValue="grades" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="grades">Grades</TabsTrigger>
                    <TabsTrigger value="subjects">Subjects</TabsTrigger>
                </TabsList>
                <TabsContent value="grades" className="flex-1">
                    <GradeDetails detailAcademicYears={detailAcademicYears} />
                </TabsContent>
                <TabsContent value="subjects" className="flex-1">
                    <SubjectDetails detailAcademicYears={detailAcademicYears} />
                </TabsContent>
            </Tabs>

            {/* Metadata */}
            <Card>
                <CardHeader>
                    <CardTitle>Configuration History</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-gray-600">Created:</span>
                            <div className="font-medium">{formatDate(detailAcademicYears.createdAt)}</div>
                        </div>
                        <div>
                            <span className="text-gray-600">Last Updated:</span>
                            <div className="font-medium">{formatDate(detailAcademicYears.updatedAt)}</div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

function GradeDetails({ detailAcademicYears }: { detailAcademicYears: DetailAcademicYear }) {
    const fetchGrade = async (gradeId: string) => {
        const sectionFields = ["id", "section"] as const
        const subjectFields = ["id", "name", "code"] as const
        const streamFields = ["id", "name",] as const
        const selectedSchema = z.object({
            sections: z.array(pickFields(SectionSchema, sectionFields)),
            subjects: z.array(pickFields(SubjectSchema, subjectFields)),
            streams: z.array(pickFields(StreamSchema, streamFields)),
        });

        const response = await sharedApi.getGradeDetail(gradeId, selectedSchema, {
            expand: ["sections", "subjects", "streams"],
            nestedFields: { "sections": [...sectionFields], "subjects": [...subjectFields], "streams": [...streamFields] },
        });

        if (!response.success) {
            toast.error(response.error.message, {
                style: { color: "red" },
            });
            throw new Error("Failed to fetch Grade detail: " + response.error.message);

        }
        return response.data;
    };

    const gradeQueries = useQueries({
        queries: detailAcademicYears.grades.map((grade) => ({
            queryKey: ['grade-detail', grade.id],
            queryFn: () => fetchGrade(grade.id),
            onError: (err: any) => {
                toast.error(err.message || 'Failed to fetch Grade detail', {
                    style: { color: 'red' },
                })
            },
            enabled: !!detailAcademicYears.grades.length,
        })),
    });

    const detailGrade: DetailGrade[] = gradeQueries
        .map((query) => query.data)
        .filter(Boolean) as DetailGrade[];

    return <Card>
        <CardHeader>
            <CardTitle className="flex items-center gap-2">
                <GraduationCap className="h-5 w-5" />
                Grades & Academic Streams ({detailAcademicYears.grades.length})
            </CardTitle>
        </CardHeader>
        <FadeIn isLoading={!(detailAcademicYears.grades.length === detailGrade.length)} loader={<CardSkeleton />}>
            <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {detailGrade.map((grade) => (
                        <Card key={grade.id} className="border-l-4 border-l-blue-500">
                            <CardHeader className="pb-1">
                                <CardTitle className="flex items-center gap-2">
                                    <GraduationCap className="h-5 w-5" />
                                    Grade {grade.grade}
                                </CardTitle>
                                <div className="flex items-center gap-1">
                                    <Badge variant="outline" className="flex items-center gap-1">
                                        <Users className="h-3 w-3" />
                                        {grade.level}
                                    </Badge>
                                    <Badge variant="outline" className="flex items-center gap-1">
                                        <Users className="h-3 w-3" />
                                        {grade.sections.length} Sections
                                    </Badge>
                                    {grade.hasStream && (
                                        <Badge variant="destructive" className="flex items-center gap-1">
                                            <Layers className="h-3 w-3" />
                                            {grade.streams.length} Streams
                                        </Badge>
                                    )}
                                </div>
                            </CardHeader>
                            <CardContent className="p-4">
                                {/* Sections */}
                                <div className="mb-3">
                                    <h5 className="font-medium text-sm mb-2">Sections:</h5>
                                    <div className="flex flex-wrap gap-1">
                                        {grade.sections.map((section) => (
                                            <Badge key={section.id} variant="outline" className="text-xs">
                                                Section {section.section}
                                            </Badge>
                                        ))}
                                    </div>
                                </div>
                                {/* Streams */}
                                {grade.hasStream && grade.streams.length > 0 && (
                                    <div>
                                        <h5 className="font-medium text-sm mb-2">Academic Streams:</h5>
                                        <div className="space-y-2">
                                            {grade.streams.map((stream) => (
                                                <Card key={stream.id} className="border-l-4 border-l-red-400">
                                                    <div className="bg-gray-50 p-3 rounded-lg">
                                                        <div className="flex items-center justify-between mb-2">
                                                            <div>
                                                                <h6 className="font-medium">{stream.name}</h6>
                                                                {/* <p className="text-sm text-gray-600">{stream.description}</p> */}
                                                            </div>
                                                            <Badge variant="outline">{stream.name}</Badge>
                                                        </div>
                                                    </div>
                                                </Card>
                                            ))}
                                        </div>
                                    </div>
                                )}
                                {/* Grade Subjects (for non-stream grades) */}
                                {!grade.hasStream && (
                                    <div>
                                        <h5 className="font-medium text-sm mb-2">Subjects:</h5>
                                        <div className="flex flex-wrap gap-1">
                                            {grade.subjects.map((subject) => (
                                                <Badge key={subject.id} variant="secondary" className="text-xs">
                                                    {subject.name}
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
        </FadeIn>
    </Card>
}



function SubjectDetails({ detailAcademicYears }: { detailAcademicYears: DetailAcademicYear }) {
    const fetchSubject = async (subjectId: string) => {
        const gradeFields = ["id", "grade"] as const
        const streamFields = ["id", "name"] as const
        const selectedSchema = z.object({
            grades: z.array(pickFields(GradeSchema, gradeFields)),
            streams: z.array(pickFields(StreamSchema, streamFields)),
        });

        const response = await sharedApi.getSubjectDetail(subjectId, selectedSchema, {
            expand: ["grades", "streams"],
            nestedFields: { "grades": [...gradeFields], "streams": [...streamFields] },
        });

        if (!response.success) {
            toast.error(response.error.message, {
                style: { color: "red" },
            });
            throw new Error(response.error.message);
        }
        return response.data;
    };


    const subjectQueries = useQueries({
        queries: detailAcademicYears.subjects.map((subject) => ({
            queryKey: ['subject-detail', subject.id],
            queryFn: () => fetchSubject(subject.id),
            onError: (err: any) => {
                toast.error(err.message || 'Failed to fetch subject detail', {
                    style: { color: 'red' },
                })
            },
            enabled: !!detailAcademicYears.subjects.length,
        })),
    })

    const detailSubject: DetailSubject[] = subjectQueries
        .map((query) => query.data)
        .filter(Boolean) as DetailSubject[]

    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <BookOpen className="h-5 w-5" />
                    Subjects ({detailAcademicYears.subjects.length})
                </CardTitle>
            </CardHeader>
            <FadeIn isLoading={!(detailAcademicYears.subjects.length === detailSubject.length)} loader={<CardSkeleton />}>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {detailSubject.map((subject) => (
                            <Card
                                key={subject.id}
                                className="hover:shadow-lg transition-shadow flex flex-col">
                                <CardHeader className="pb-3">
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <CardTitle className="flex items-center gap-2 mb-2">
                                                <BookOpen className="h-5 w-5" />
                                                {subject.name}
                                            </CardTitle>
                                        </div>
                                        <Badge variant="outline" className="flex items-center gap-1">
                                            {subject.code}
                                        </Badge>
                                        {/* <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button variant="ghost" size="sm">
                                        <MoreHorizontal className="h-4 w-4" />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end">
                                    <DropdownMenuItem onClick={() => onView(subject)}>
                                        <Eye className="h-4 w-4 mr-2" />
                                        View Details
                                    </DropdownMenuItem>
                                    <DropdownMenuItem onClick={() => onEdit(subject)}>
                                        <Edit className="h-4 w-4 mr-2" />
                                        Edit Subject
                                    </DropdownMenuItem>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuItem onClick={() => onDelete(subject)} className="text-red-600">
                                        <Trash2 className="h-4 w-4 mr-2" />
                                        Delete Subject
                                    </DropdownMenuItem>
                                </DropdownMenuContent>
                            </DropdownMenu> */}
                                    </div>
                                </CardHeader>
                                <CardContent className="space-y-4 flex-grow">
                                    {/* Assignment Stats */}
                                    <div className="grid grid-cols-2 gap-2">
                                        <div className="text-center p-2 bg-blue-50 rounded-lg">
                                            <GraduationCap className="h-4 w-4 text-blue-600 mx-auto mb-1" />
                                            <div className="text-sm font-semibold text-blue-900">{subject.grades.length}</div>
                                            <div className="text-xs text-blue-700">Grades</div>
                                        </div>
                                        <div className="text-center p-2 bg-purple-50 rounded-lg">
                                            <Users className="h-4 w-4 text-purple-600 mx-auto mb-1" />
                                            <div className="text-sm font-semibold text-purple-900">{2}</div>
                                            <div className="text-xs text-purple-700">Streams</div>
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between">
                                        <div className="flex-col items-center gap-2 flex-wrap mt-2">
                                            <h4 className="text-sm font-medium mb-2">Taught In:</h4>
                                            <div className="flex flex-wrap gap-1">
                                                {subject.grades.map((grade) => (
                                                    <Badge
                                                        key={grade.id}
                                                        variant="secondary"
                                                    >
                                                        Grade {grade.grade}
                                                    </Badge>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </CardContent>
                                <CardFooter>
                                    <div className="flex flex-col gap-2 w-full">
                                        {/* Last Updated */}
                                        <div className="text-xs text-gray-500 pt-2 border-t">
                                            Updated: {new Date().toLocaleDateString()}
                                        </div>
                                        {/* Action Buttons */}
                                        <div className="flex gap-2 bottom-0">
                                            <Button variant="outline" size="sm" onClick={() => { }} className="flex-1 bg-transparent">
                                                <Eye className="h-4 w-4 mr-2" />
                                                View
                                            </Button>
                                            <Button variant="outline" size="sm" onClick={() => { }} className="flex-1 bg-transparent">
                                                <Edit className="h-4 w-4 mr-2" />
                                                Edit
                                            </Button>
                                        </div>
                                    </div>
                                </CardFooter>
                            </Card>
                        ))}
                    </div>
                </CardContent>
            </FadeIn>
        </Card>
    )
}


function CardSkeleton() {
    return (
        <Card>
            <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[...Array(6)].map((_, i) => (
                        <Card key={i}>
                            <CardHeader className="pb-1 space-y-2">
                                <CardTitle className="flex items-center gap-2">
                                    <Skeleton className="h-5 w-24" />
                                </CardTitle>
                                <div className="flex items-center gap-1 flex-wrap">
                                    <Skeleton className="h-6 w-20 rounded" />
                                    <Skeleton className="h-6 w-24 rounded" />
                                    <Skeleton className="h-6 w-24 rounded" />
                                </div>
                            </CardHeader>

                            <CardContent className="p-4 space-y-4">
                                {/* Sections */}
                                <div>
                                    <Skeleton className="h-4 w-24 mb-2" />
                                    <div className="flex flex-wrap gap-1">
                                        {[...Array(3)].map((_, j) => (
                                            <Skeleton key={j} className="h-5 w-16 rounded" />
                                        ))}
                                    </div>
                                </div>

                                {/* Streams */}
                                <div>
                                    <Skeleton className="h-4 w-32 mb-2" />
                                    <div className="space-y-2">
                                        {[...Array(0)].map((_, k) => (
                                            <Card key={k}>
                                                <div className="p-3 rounded-lg space-y-2">
                                                    <div className="flex items-center justify-between">
                                                        <Skeleton className="h-4 w-24" />
                                                        <Skeleton className="h-5 w-16 rounded" />
                                                    </div>
                                                    <div>
                                                        <Skeleton className="h-4 w-20 mb-1" />
                                                        <div className="flex flex-wrap gap-1">
                                                            {[...Array(2)].map((_, m) => (
                                                                <Skeleton key={m} className="h-5 w-20 rounded" />
                                                            ))}
                                                        </div>
                                                    </div>
                                                </div>
                                            </Card>
                                        ))}
                                    </div>
                                </div>

                                {/* Subjects (non-stream) */}
                                <div>
                                    <Skeleton className="h-4 w-24 mb-2" />
                                    <div className="flex flex-wrap gap-1">
                                        {[...Array(3)].map((_, j) => (
                                            <Skeleton key={j} className="h-5 w-20 rounded" />
                                        ))}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </CardContent>
        </Card>
    );
}
