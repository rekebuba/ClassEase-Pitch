import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { SelectItem } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar, GraduationCap, BookOpen, Settings, Plus, Save, Eye } from "lucide-react"
import { SubjectManagement } from "@/components"
import { allSubjects, getDefaultSections, getGradeLevel, getStreamsByGrade, getSubjectsByGrade, hasStreamByGrade } from "@/config/suggestion"
import { DetailAcademicYear } from "@/components/academic-year-view-card"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { GradeSchema, SectionSchema, StreamSchema, SubjectSchema, YearSetupSchema } from "@/lib/api-response-validation"
import type { Stream, Grade, Section, YearSetupType, Subject } from "@/lib/api-response-type"
import { Form } from "@/components/ui/form"
import { InputWithLabel } from "@/components/inputs/input-labeled"
import { DateWithLabel } from "@/components/inputs/date-labeled"
import { SelectWithLabel } from "@/components/inputs/select-labeled"
import GradeManagement from "@/components/grade-management"
import z from "zod"
import { pickFields } from "@/utils/pick-zod-fields"
import sharedApi from "@/api/sharedApi"
import { toast } from "sonner"

interface AcademicYearSetupProps {
    initialData: DetailAcademicYear
    onSave?: (academicYear: DetailAcademicYear) => void
    onCancel?: () => void
    mode?: "create" | "edit"
}

type PickSubject = Pick<Subject, "id" | "name" | "code">
type PickStream = Pick<Stream, "id" | "name">
type PickSection = Pick<Section, "id" | "section">
type GradeRelation = {
    sections: PickSection[]
    streams: PickStream[]
    subjects: PickSubject[]
}

type StreamRelation = {
    subjects: PickSubject[]
}

export default function AcademicYearSetup({
    initialData,
    onSave,
    onCancel,
    mode = "create",
}: AcademicYearSetupProps) {
    const [academicYear, setAcademicYear] = useState<Partial<DetailAcademicYear>>(initialData);
    const [dayDifference, setDayDifference] = useState<number | null>(null);

    const [activeTab, setActiveTab] = useState("basic")

    const [defaultNestedGrade, setDefaultNestedGrade] = useState<YearSetupType["grades"]>([])

    // --- Util functions
    const getDetailStream = async (streamId: string): Promise<StreamRelation | undefined> => {
        // const subjectFields = ["id", "name", "code"] as const
        const schema = z.object({
            subjects: z.array(SubjectSchema),
        })

        const response = await sharedApi.getStreamDetail(streamId, schema, {
            expand: ["subjects"],
            nestedFields: { subjects: SubjectSchema.keyof().options },
        })

        if (!response.success) {
            toast.error(response.error.message, { style: { color: "red" } })
            return
        }

        return response.data
    }

    const fetchGrade = async (gradeId: string): Promise<GradeRelation | undefined> => {
        // const sectionFields = ["id", "section"] as const
        // const subjectFields = ["id", "name", "code"] as const
        // const streamFields = ["id", "name"] as const

        const schema = z.object({
            sections: z.array(SectionSchema),
            subjects: z.array(SubjectSchema),
            streams: z.array(StreamSchema),
        })

        const response = await sharedApi.getGradeDetail(gradeId, schema, {
            expand: ["sections", "subjects", "streams"],
            nestedFields: {
                sections: SectionSchema.keyof().options,
                subjects: SubjectSchema.keyof().options,
                streams: StreamSchema.keyof().options,
            },
        })

        if (!response.success) {
            toast.error(response.error.message, { style: { color: "red" } })
            return
        }

        return response.data
    }


    const generateDefaultGrades = async () => {
        if (!initialData?.grades) return

        const results = await Promise.all(
            initialData.grades.map(async (grade) => {
                const fetchedGrade = await fetchGrade(grade.id)
                if (!fetchedGrade) return null

                const detailedStreams = await Promise.all(
                    fetchedGrade.streams.map(async (stream) => {
                        const detailed = await getDetailStream(stream.id)
                        return { ...stream, ...detailed }
                    })
                )

                return {
                    ...fetchedGrade,
                    ...grade,
                    streams: detailedStreams,
                }
            })
        )

        const cleaned = results.filter(Boolean) as YearSetupType["grades"]
        setDefaultNestedGrade(cleaned)
    }

    useEffect(() => {
        if (initialData?.grades && mode !== "create") {
            generateDefaultGrades()
        } else {
            // fallback: generate 12 empty grades
            const grades = Array.from({ length: 12 }, (_, i) => ({
                id: crypto.randomUUID(),
                yearId: "",
                grade: `Grade ${i + 1}`,
                level: getGradeLevel(i + 1),
                hasStream: hasStreamByGrade(i + 1),
                streams: getStreamsByGrade(i + 1),
                sections: getDefaultSections(),
                subjects: i + 1 < 11 ? getSubjectsByGrade(i + 1) : [],
            }))
            setDefaultNestedGrade(grades)
        }
    }, [])

    const defaultValues: YearSetupType = {
        year: {
            id: initialData ? initialData.id : crypto.randomUUID(),
            calendarType: initialData ? initialData.calendarType : "" as "Semester",
            name: initialData ? initialData.name : "",
            startDate: initialData ? initialData.startDate : "",
            endDate: initialData ? initialData.endDate : "",
            status: initialData ? initialData.status : "",
            createdAt: initialData ? initialData.createdAt : "",
            updatedAt: initialData ? initialData.updatedAt : ""
        },
        grades: defaultNestedGrade,
        subjects: initialData ? initialData.subjects : allSubjects,
    }

    const form = useForm<YearSetupType>({
        resolver: zodResolver(YearSetupSchema),
        defaultValues
    })
    const watchForm = form.watch()

    function submitForm(values: YearSetupType) {
        console.log("Submitted values:", values)
    }

    useEffect(() => {
        if (watchForm.year.startDate && watchForm.year.endDate) {
            const start = new Date(watchForm.year.startDate);
            const end = new Date(watchForm.year.endDate);
            const diffInDays = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
            setDayDifference(diffInDays);
            if (watchForm.year.startDate > watchForm.year.endDate) {
                form.setValue("year.endDate", "");
            }
        } else {
            setDayDifference(null);
        }
    }, [watchForm.year.startDate, watchForm.year.endDate]);

    console.log("watchForm:", watchForm)
    console.log("defaultNestedGrade: ", defaultNestedGrade)

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
            <div className="max-w-7xl mx-auto space-y-6">
                {/* Header */}
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">
                            {mode === "edit" ? "Edit Academic Year" : "Academic Year Setup"}
                        </h1>
                        <p className="text-gray-600 mt-1">
                            {mode === "edit"
                                ? "Modify your academic year configuration"
                                : "Configure your school's academic year structure"}
                        </p>
                    </div>
                    <div className="flex items-center gap-3">
                        {onCancel && (
                            <Button variant="outline" onClick={onCancel}>
                                Cancel
                            </Button>
                        )}
                        <Button variant="outline">
                            <Eye className="h-4 w-4 mr-2" />
                            Preview
                        </Button>
                        <Button>
                            <Save className="h-4 w-4 mr-2" />
                            {mode === "edit" ? "Update Academic Year" : "Save Academic Year"}
                        </Button>
                    </div>
                </div>

                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(submitForm)}
                    // className="flex flex-col md:flex-row gap-4 md:gap-8"
                    >
                        {/* Main Content */}
                        <Tabs value={activeTab} onValueChange={setActiveTab}>
                            <TabsList className="grid w-full grid-cols-3">
                                <TabsTrigger value="basic" className="flex items-center gap-2">
                                    <Calendar className="h-4 w-4" />
                                    Basic Info
                                </TabsTrigger>
                                <TabsTrigger value="subjects" className="flex items-center gap-2">
                                    <BookOpen className="h-4 w-4" />
                                    Subjects
                                </TabsTrigger>
                                <TabsTrigger value="grades" className="flex items-center gap-2">
                                    <GraduationCap className="h-4 w-4" />
                                    Grades & Streams
                                </TabsTrigger>
                            </TabsList>

                            {/* Basic Information Tab */}
                            <TabsContent value="basic" className="space-y-6">
                                <Card>
                                    <CardHeader>
                                        <CardTitle>Academic Year Basic Information</CardTitle>
                                        <p className="text-sm text-gray-600">Set up the fundamental details of your academic year</p>
                                    </CardHeader>
                                    <CardContent className="space-y-6">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                            <InputWithLabel
                                                fieldTitle="Academic Year Name"
                                                nameInSchema="year.name"
                                                placeholder="e.g., 2024-2025 Academic Year"
                                            />

                                            <SelectWithLabel
                                                fieldTitle="Term System"
                                                nameInSchema="year.calendarType"
                                            >
                                                <SelectItem value="Semester">Semester (2 Terms)</SelectItem>
                                                <SelectItem value="Quarter">Quarterly (4 Terms)</SelectItem>
                                            </SelectWithLabel>
                                        </div>

                                        <div className="flex items-center gap-3 flex-wrap">
                                            <div className="flex-1 min-w-0">
                                                <DateWithLabel
                                                    fieldTitle="Academic Year Start Date"
                                                    nameInSchema="year.startDate"
                                                />
                                            </div>

                                            {/* Calculate Date Range */}
                                            <Badge
                                                variant={dayDifference && dayDifference < 0 ? "destructive" : "outline"}
                                                className="whitespace-nowrap mt-7"
                                            >
                                                {dayDifference !== null ? `${dayDifference} d` : '--'}
                                            </Badge>

                                            <div className="flex-1 min-w-0">
                                                <DateWithLabel
                                                    fieldTitle="Academic Year End Date"
                                                    nameInSchema="year.endDate"
                                                    className="flex-1 min-w-0"
                                                    disableFrom={watchForm.year.startDate ? new Date(watchForm.year.startDate) : new Date("1900-01-01")}
                                                />
                                            </div>
                                        </div>
                                    </CardContent>
                                </Card>
                            </TabsContent>

                            {/* Grades & Streams Tab */}
                            <TabsContent value="grades" className="space-y-6">
                                {/* Grades List */}
                                <GradeManagement form={form} />
                                {/* <GradeSetupCard form={form} /> */}

                                {academicYear.grades?.length === 0 && (
                                    <div className="text-center py-12 text-gray-500">
                                        <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                        <p>No grades configured yet. Add your first grade level above.</p>
                                    </div>
                                )}
                            </TabsContent>

                            {/* Subjects Tab */}
                            <TabsContent value="subjects" className="space-y-6">
                                <SubjectManagement form={form} />
                            </TabsContent>
                            {/* Deleted Tabs */}
                        </Tabs>
                    </form>
                </Form>
            </div>
        </div >
    )
}
