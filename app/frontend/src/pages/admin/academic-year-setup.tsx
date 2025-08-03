import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar, GraduationCap, BookOpen, Settings, Plus, Save, Eye } from "lucide-react"
import { GradeSetupCard } from "@/components"
import { SubjectManagement } from "@/components"
import { allSubjects, allSubjectsData, getStreamsByGrade, getSubjectsByGrade, hasStreamByGrade } from "@/config/suggestion"
import { DetailAcademicYear } from "@/components/academic-year-view-card"
import { zodResolver } from "@hookform/resolvers/zod"
import { useFieldArray, useForm } from "react-hook-form"
import { YearSetupSchema, YearSchema } from "@/lib/api-response-validation"
import { Grade, Subject, Stream, Section, Year, YearSetupType } from "@/lib/api-response-type"
import { Form } from "@/components/ui/form"
import { InputWithLabel } from "@/components/inputs/input-labeled"
import { SelectWithLabel } from "@/components/inputs/select-labeled"
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled"

interface AcademicYearSetupProps {
    initialData: DetailAcademicYear
    onSave?: (academicYear: DetailAcademicYear) => void
    onCancel?: () => void
    mode?: "create" | "edit"
}

export default function AcademicYearSetup({
    initialData,
    onSave,
    onCancel,
    mode = "create",
}: AcademicYearSetupProps) {
    // const [suggestedSubjects, setSuggestedSubjects] = useState<Subject[]>(AllSubjects.map((subject) => ({
    //     id: crypto.randomUUID(),
    //     name: subject.subject,
    //     code: subject.codes,
    //     grades: subject.grades,
    // })))
    const [academicYear, setAcademicYear] = useState<Partial<DetailAcademicYear>>(initialData);
    const [dayDifference, setDayDifference] = useState<number | null>(null);

    const [activeTab, setActiveTab] = useState("basic")

    const updateAcademicYear = (updates: Partial<DetailAcademicYear>) => {
        setAcademicYear({ ...academicYear, ...updates })
    }

    const updateGrade = (gradeId: string, updatedGrade: Grade) => {
        console.log("Updating grade:", gradeId, updatedGrade)
        // updateAcademicYear({
        //     grades: academicYear.grades?.map((g) => (g.id === gradeId ? updatedGrade : g)) || [],
        // })
    }

    // const removeGrade = (gradeId: string) => {
    //     console.log("Removing grade:", gradeId)
    //     // updateAcademicYear({
    //     //     grades: academicYear.grades?.filter((g) => g.id !== gradeId) || [],
    //     // })
    // }

    const generateAcademicYearName = () => {
        if (academicYear.startDate) {
            const startYear = new Date(academicYear.startDate).getFullYear()
            const endYear = startYear + 1
            return `${startYear}-${endYear} Academic Year`
        }
        return ""
    }

    const validateForm = () => {
        return !!(
            academicYear.name &&
            academicYear.startDate &&
            academicYear.endDate &&
            academicYear.grades?.length &&
            academicYear.subjects?.length
        )
    }

    const saveAcademicYear = () => {
        console.log("Saving academic year:", academicYear)
        // if (validateForm()) {
        //     const completeAcademicYear: DetailAcademicYear = {
        //         id: initialData?.id || Date.now().toString(),
        //         name: academicYear.name!,
        //         startDate: academicYear.startDate!,
        //         endDate: academicYear.endDate!,
        //         termSystem: academicYear.termSystem!,
        //         status: academicYear.status || "draft",
        //         grades: academicYear.grades || [],
        //         subjects: academicYear.subjects || [],
        //         createdAt: initialData?.createdAt || new Date().toISOString(),
        //         updatedAt: new Date().toISOString(),
        //     }

        //     if (onSave) {
        //         onSave(completeAcademicYear)
        //     } else {
        //         console.log("Saving Academic Year:", completeAcademicYear)
        //         alert("Academic Year setup saved successfully!")
        //     }
        // } else {
        //     alert("Please fill in all required fields")
        // }
    }



    const previewAcademicYear = () => {
        console.log("Academic Year Preview:", academicYear)
        // Here you would show a preview modal or navigate to preview page
    }

    function generateDefaultSection(): Section {
        return {
            id: "",
            gradeId: "",
            section: "",
        }
    }
    function generateDefaultSubject(): Subject[] {
        return allSubjects
    }
    function generateDefaultStream(): YearSetupType["grades"][number]["streams"] {
        return []
    }

    function generateDefaultGrades(): YearSetupType["grades"] {
        return Array.from({ length: 12 }, (_, i) => ({
            id: "",
            yearId: "",
            grade: `Grade ${i + 1}`,
            level: "" as "primary",
            hasStream: hasStreamByGrade(i + 1),
            streams: getStreamsByGrade(i + 1),
            sections: [generateDefaultSection()],
            subjects: getSubjectsByGrade(i + 1),
        }))
    }

    const defaultValues = {
        year: {
            id: "",
            calendarType: "" as "Semester",
            name: "",
            startDate: "",
            endDate: "",
            createdAt: "",
            updatedAt: ""
        },
        grades: generateDefaultGrades(),
        subjects: generateDefaultSubject(),
    }

    const form = useForm<YearSetupType>({
        resolver: zodResolver(YearSetupSchema),
        defaultValues
    })
    const watchForm = form.watch()

    const {
        fields: gradeFields,
        append: appendGrade,
        remove: removeGrade,
    } = useFieldArray({
        control: form.control,
        name: "grades",
    })

    function submitForm(values: YearSetupType) {
        console.log("Submitted values:", values)
    }

    useEffect(() => {
        if (watchForm.year.startDate && watchForm.year.endDate) {
            const start = new Date(watchForm.year.startDate);
            const end = new Date(watchForm.year.endDate);
            const diffInDays = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
            setDayDifference(diffInDays);
        } else {
            setDayDifference(null);
        }
    }, [watchForm.year.startDate, watchForm.year.endDate]);

    console.log("watchForm:", watchForm)

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
                        <Button variant="outline" onClick={previewAcademicYear}>
                            <Eye className="h-4 w-4 mr-2" />
                            Preview
                        </Button>
                        <Button onClick={saveAcademicYear} disabled={!validateForm()}>
                            <Save className="h-4 w-4 mr-2" />
                            {mode === "edit" ? "Update Academic Year" : "Save Academic Year"}
                        </Button>
                    </div>
                </div>

                {/* Progress Indicator */}
                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between text-sm">
                            <div className="flex items-center gap-2">
                                <div
                                    className={`w-3 h-3 rounded-full ${academicYear.name && academicYear.startDate && academicYear.endDate ? "bg-green-500" : "bg-gray-300"}`}
                                />
                                <span>Basic Info</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div
                                    className={`w-3 h-3 rounded-full ${academicYear.subjects?.length ? "bg-green-500" : "bg-gray-300"}`}
                                />
                                <span>Subjects</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div
                                    className={`w-3 h-3 rounded-full ${academicYear.grades?.length ? "bg-green-500" : "bg-gray-300"}`}
                                />
                                <span>Grades & Streams</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <div className={`w-3 h-3 rounded-full ${validateForm() ? "bg-green-500" : "bg-gray-300"}`} />
                                <span>Complete</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Form {...form}>
                    <form
                        onSubmit={form.handleSubmit(submitForm)}
                    // className="flex flex-col md:flex-row gap-4 md:gap-8"
                    >
                        {/* Main Content */}
                        <Tabs value={activeTab} onValueChange={setActiveTab}>
                            <TabsList className="grid w-full grid-cols-4">
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
                                <TabsTrigger value="review" className="flex items-center gap-2">
                                    <Settings className="h-4 w-4" />
                                    Review & Finalize
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
                                        <div className="flex items-center gap-3 flex-wrap">
                                            <div className="flex-1 min-w-0">
                                                <InputWithLabel
                                                    fieldTitle="Academic Year Start Date"
                                                    type="date"
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
                                                <InputWithLabel
                                                    fieldTitle="Academic Year End Date"
                                                    type="date"
                                                    nameInSchema="year.endDate"
                                                    className="flex-1 min-w-0"
                                                />
                                            </div>
                                        </div>

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


                                    </CardContent>
                                </Card>
                            </TabsContent>

                            {/* Grades & Streams Tab */}
                            <TabsContent value="grades" className="space-y-6">
                                {/* Grades List */}
                                <GradeSetupCard form={form} />

                                {academicYear.grades?.length === 0 && (
                                    <div className="text-center py-12 text-gray-500">
                                        <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                        <p>No grades configured yet. Add your first grade level above.</p>
                                    </div>
                                )}
                            </TabsContent>

                            {/* Subjects Tab */}
                            <TabsContent value="subjects" className="space-y-6">
                                <SubjectManagement
                                    form={form}
                                />
                            </TabsContent>
                            {/* Deleted Tabs */}
                        </Tabs>
                    </form>
                </Form>
            </div>
        </div >
    )
}
