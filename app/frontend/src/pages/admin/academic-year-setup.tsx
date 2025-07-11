import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Calendar, GraduationCap, BookOpen, Settings, Plus, Save, Eye } from "lucide-react"
import type { AcademicYear, Grade, Subject } from "@/lib/academic-year"
import { GRADE_SUGGESTIONS } from "@/lib/academic-year"
import { GradeSetupCard } from "@/components"
import { SubjectManagement } from "@/components"
import { AllSubjects } from "@/config/suggestion"

interface AcademicYearSetupProps {
    initialData?: AcademicYear
    onSave?: (academicYear: AcademicYear) => void
    onCancel?: () => void
    mode?: "create" | "edit"
}

export default function AcademicYearSetup({
    initialData,
    onSave,
    onCancel,
    mode = "create",
}: AcademicYearSetupProps = {}) {
    const [suggestedSubjects, setSuggestedSubjects] = useState<Subject[]>(AllSubjects.map((subject) => ({
        id: crypto.randomUUID(),
        name: subject.subject,
        code: subject.codes,
        grades: subject.grades,
    })))
    const [academicYear, setAcademicYear] = useState<Partial<AcademicYear>>(
        initialData || {
            name: "",
            startDate: "",
            endDate: "",
            termSystem: "semesterly",
            status: "draft",
            grades: [],
            subjects: suggestedSubjects,
        },
    )

    const [activeTab, setActiveTab] = useState("basic")

    const updateAcademicYear = (updates: Partial<AcademicYear>) => {
        setAcademicYear({ ...academicYear, ...updates })
    }

    const addGrade = (gradeSuggestion?: (typeof GRADE_SUGGESTIONS)[0]) => {
        const newGrade: Grade = {
            id: Date.now().toString(),
            name: gradeSuggestion?.name || `Grade ${(academicYear.grades?.length || 0) + 1}`,
            level: gradeSuggestion?.level || (academicYear.grades?.length || 0) + 1,
            hasStreams: gradeSuggestion?.hasStreams || false,
            streams: [],
            maxSections: 2,
            sections: ["A", "B"],
            subjects: gradeSuggestion?.defaultSubjects || [],
        }
        updateAcademicYear({ grades: [...(academicYear.grades || []), newGrade] })
    }

    const updateGrade = (gradeId: string, updatedGrade: Grade) => {
        updateAcademicYear({
            grades: academicYear.grades?.map((g) => (g.id === gradeId ? updatedGrade : g)) || [],
        })
    }

    const removeGrade = (gradeId: string) => {
        updateAcademicYear({
            grades: academicYear.grades?.filter((g) => g.id !== gradeId) || [],
        })
    }

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
        if (validateForm()) {
            const completeAcademicYear: AcademicYear = {
                id: initialData?.id || Date.now().toString(),
                name: academicYear.name!,
                startDate: academicYear.startDate!,
                endDate: academicYear.endDate!,
                termSystem: academicYear.termSystem!,
                status: academicYear.status || "draft",
                grades: academicYear.grades || [],
                subjects: academicYear.subjects || [],
                createdAt: initialData?.createdAt || new Date().toISOString(),
                updatedAt: new Date().toISOString(),
            }

            if (onSave) {
                onSave(completeAcademicYear)
            } else {
                console.log("Saving Academic Year:", completeAcademicYear)
                alert("Academic Year setup saved successfully!")
            }
        } else {
            alert("Please fill in all required fields")
        }
    }

    const previewAcademicYear = () => {
        console.log("Academic Year Preview:", academicYear)
        // Here you would show a preview modal or navigate to preview page
    }

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
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div>
                                        <Label htmlFor="start-date">Academic Year Start Date</Label>
                                        <Input
                                            id="start-date"
                                            type="date"
                                            value={academicYear.startDate || ""}
                                            onChange={(e) => {
                                                updateAcademicYear({ startDate: e.target.value })
                                                if (!academicYear.name) {
                                                    setTimeout(() => {
                                                        updateAcademicYear({ name: generateAcademicYearName() })
                                                    }, 100)
                                                }
                                            }}
                                        />
                                    </div>
                                    <div>
                                        <Label htmlFor="end-date">Academic Year End Date</Label>
                                        <Input
                                            id="end-date"
                                            type="date"
                                            value={academicYear.endDate || ""}
                                            onChange={(e) => updateAcademicYear({ endDate: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div>
                                    <Label htmlFor="year-name">Academic Year Name</Label>
                                    <Input
                                        id="year-name"
                                        value={academicYear.name || ""}
                                        onChange={(e) => updateAcademicYear({ name: e.target.value })}
                                        placeholder="e.g., 2024-2025 Academic Year"
                                    />
                                    {academicYear.startDate && (
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            className="mt-2 bg-transparent"
                                            onClick={() => updateAcademicYear({ name: generateAcademicYearName() })}
                                        >
                                            Auto-generate Name
                                        </Button>
                                    )}
                                </div>

                                <div>
                                    <Label>Term System</Label>
                                    <Select
                                        value={academicYear.termSystem}
                                        onValueChange={(value: "quarterly" | "semesterly") => updateAcademicYear({ termSystem: value })}
                                    >
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="semesterly">
                                                <div>
                                                    <div className="font-medium">Semesterly (2 Terms)</div>
                                                    <div className="text-sm text-gray-500">Fall Semester & Spring Semester</div>
                                                </div>
                                            </SelectItem>
                                            <SelectItem value="quarterly">
                                                <div>
                                                    <div className="font-medium">Quarterly (4 Terms)</div>
                                                    <div className="text-sm text-gray-500">Fall, Winter, Spring, Summer Quarters</div>
                                                </div>
                                            </SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                {/* Academic Year Summary */}
                                {academicYear.startDate && academicYear.endDate && (
                                    <Card className="bg-blue-50 border-blue-200">
                                        <CardContent className="p-4">
                                            <h4 className="font-medium mb-2">Academic Year Summary</h4>
                                            <div className="grid grid-cols-2 gap-4 text-sm">
                                                <div>
                                                    <span className="text-gray-600">Duration:</span>
                                                    <div className="font-medium">
                                                        {Math.ceil(
                                                            (new Date(academicYear.endDate).getTime() - new Date(academicYear.startDate).getTime()) /
                                                            (1000 * 60 * 60 * 24),
                                                        )}{" "}
                                                        days
                                                    </div>
                                                </div>
                                                <div>
                                                    <span className="text-gray-600">Term System:</span>
                                                    <div className="font-medium capitalize">{academicYear.termSystem}</div>
                                                </div>
                                            </div>
                                        </CardContent>
                                    </Card>
                                )}
                            </CardContent>
                        </Card>
                    </TabsContent>

                    {/* Grades & Streams Tab */}
                    <TabsContent value="grades" className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Grade Levels & Academic Streams</CardTitle>
                                <p className="text-sm text-gray-600">Configure the grade levels and academic tracks for your school</p>
                            </CardHeader>
                            <CardContent>
                                {/* Quick Add Grades */}
                                <div className="mb-6">
                                    <Label className="text-base font-medium">Quick Add Grades</Label>
                                    <p className="text-sm text-gray-600 mb-3">Add common grade levels with pre-configured subjects</p>
                                    <div className="flex flex-wrap gap-2">
                                        {GRADE_SUGGESTIONS.map((grade) => (
                                            <Button
                                                key={grade.name}
                                                variant="outline"
                                                size="sm"
                                                onClick={() => addGrade(grade)}
                                                disabled={academicYear.grades?.some((g) => g.name === grade.name)}
                                            >
                                                <Plus className="h-4 w-4 mr-1" />
                                                {grade.name}
                                            </Button>
                                        ))}
                                    </div>
                                </div>

                                {/* Custom Grade */}
                                <div className="mb-6">
                                    <Button onClick={() => addGrade()} variant="outline">
                                        <Plus className="h-4 w-4 mr-2" />
                                        Add Custom Grade
                                    </Button>
                                </div>

                                {/* Grades List */}
                                <div className="space-y-4">
                                    {academicYear.grades?.map((grade) => (
                                        <GradeSetupCard
                                            key={grade.id}
                                            grade={grade}
                                            onUpdate={(updatedGrade) => updateGrade(grade.id, updatedGrade)}
                                            onRemove={() => removeGrade(grade.id)}
                                            availableSubjects={academicYear.subjects?.map((s) => s.name) || []}
                                        />
                                    ))}
                                </div>

                                {academicYear.grades?.length === 0 && (
                                    <div className="text-center py-12 text-gray-500">
                                        <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                        <p>No grades configured yet. Add your first grade level above.</p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </TabsContent>

                    {/* Subjects Tab */}
                    <TabsContent value="subjects" className="space-y-6">
                        <SubjectManagement
                            suggestedSubjects={suggestedSubjects}
                            subjects={academicYear.subjects || []}
                            onUpdate={(subjects) => updateAcademicYear({ subjects })}
                        />
                    </TabsContent>

                    {/* Review & Finalize Tab */}
                    <TabsContent value="review" className="space-y-6">
                        <Card>
                            <CardHeader>
                                <CardTitle>Academic Year Review</CardTitle>
                                <p className="text-sm text-gray-600">Review your academic year configuration before finalizing</p>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                {/* Basic Info Summary */}
                                <div>
                                    <h4 className="font-medium mb-3">Basic Information</h4>
                                    <div className="grid grid-cols-2 gap-4 text-sm">
                                        <div>
                                            <span className="text-gray-600">Academic Year:</span>
                                            <div className="font-medium">{academicYear.name || "Not set"}</div>
                                        </div>
                                        <div>
                                            <span className="text-gray-600">Duration:</span>
                                            <div className="font-medium">
                                                {academicYear.startDate && academicYear.endDate
                                                    ? `${academicYear.startDate} to ${academicYear.endDate}`
                                                    : "Not set"}
                                            </div>
                                        </div>
                                        <div>
                                            <span className="text-gray-600">Term System:</span>
                                            <div className="font-medium capitalize">{academicYear.termSystem}</div>
                                        </div>
                                    </div>
                                </div>

                                {/* Grades Summary */}
                                <div>
                                    <h4 className="font-medium mb-3">Grades & Streams ({academicYear.grades?.length || 0})</h4>
                                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                                        {academicYear.grades?.map((grade) => (
                                            <Card key={grade.id} className="p-3">
                                                <div className="flex items-center justify-between mb-2">
                                                    <h5 className="font-medium">{grade.name}</h5>
                                                    <Badge variant="outline">{grade.sections.length} Sections</Badge>
                                                </div>
                                                {grade.hasStreams && (
                                                    <div className="mb-2">
                                                        <div className="text-sm text-gray-600">Streams:</div>
                                                        <div className="flex flex-wrap gap-1">
                                                            {grade.streams.map((stream) => (
                                                                <Badge key={stream.id} variant="secondary" className="text-xs">
                                                                    {stream.name}
                                                                </Badge>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}
                                                <div className="text-sm text-gray-600">
                                                    {grade.hasStreams
                                                        ? `${grade.streams.reduce((acc, stream) => acc + stream.subjects.length, 0)} Total Subjects`
                                                        : `${grade.subjects.length} Subjects`}
                                                </div>
                                            </Card>
                                        ))}
                                    </div>
                                </div>

                                {/* Subjects Summary */}
                                <div>
                                    <h4 className="font-medium mb-3">Subjects ({academicYear.subjects?.length || 0})</h4>
                                    <div className="flex flex-wrap gap-2">
                                        {academicYear.subjects?.map((subject) => (
                                            <Badge key={subject.id} variant="outline" className="flex items-center gap-1">
                                                {subject.name}
                                            </Badge>
                                        ))}
                                    </div>
                                </div>

                                {/* Validation Status */}
                                <Card className={`${validateForm() ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"}`}>
                                    <CardContent className="p-4">
                                        <h4 className="font-medium mb-2">
                                            {validateForm() ? "✅ Ready to Save" : "❌ Configuration Incomplete"}
                                        </h4>
                                        <div className="text-sm">
                                            {validateForm() ? (
                                                <p>Your academic year is fully configured and ready to be saved.</p>
                                            ) : (
                                                <div>
                                                    <p className="mb-2">Please complete the following:</p>
                                                    <ul className="list-disc list-inside space-y-1">
                                                        {!academicYear.name && <li>Set academic year name</li>}
                                                        {!academicYear.startDate && <li>Set start date</li>}
                                                        {!academicYear.endDate && <li>Set end date</li>}
                                                        {!academicYear.grades?.length && <li>Add at least one grade level</li>}
                                                        {!academicYear.subjects?.length && <li>Add at least one subject</li>}
                                                    </ul>
                                                </div>
                                            )}
                                        </div>
                                    </CardContent>
                                </Card>
                            </CardContent>
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    )
}
