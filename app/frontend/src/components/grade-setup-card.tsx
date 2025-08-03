"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { SelectItem } from "@/components/ui/select"
import { Plus, X, BookOpen, Layers, ChevronDown } from "lucide-react"
import { YearSetupType } from "@/lib/api-response-type"
import { useFieldArray, UseFormReturn } from "react-hook-form"
import { SelectWithLabel } from "./inputs/select-labeled"
import { SwitchWithLabel } from "./inputs/switch-labeled"
import { CheckboxForObject } from "./inputs/checkbox-for-object"
import { getDefaultSections, getStreamsByGrade, getSubjectsByGrade, hasStreamByGrade } from "@/config/suggestion"
import { SelectForObject } from "./inputs/select-for-object"
import { toast } from "sonner"
import { InputWithLabel } from "./inputs/input-labeled"

type Grade = YearSetupType["grades"] extends Array<infer G> ? G : never
type Subject = YearSetupType["subjects"] extends Array<infer G> ? G : never

interface GradeSetupCardProps {
    form: UseFormReturn<YearSetupType>
}

export default function GradeSetupCard({ form }: GradeSetupCardProps) {
    const { fields: gradeFields, append: appendGrade, remove: removeGrade, } = useFieldArray({
        control: form.control,
        name: "grades",
    })
    const watchForm = form.watch()

    return (
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
                        {Array.from({ length: 12 }, (_, i) => (
                            <Button
                                key={i}
                                variant="outline"
                                size="sm"
                                onClick={() =>
                                    appendGrade({
                                        id: "",
                                        yearId: "",
                                        grade: `Grade ${i + 1}`,
                                        level: "primary",
                                        hasStream: hasStreamByGrade(i + 1),
                                        streams: getStreamsByGrade(i + 1),
                                        sections: getDefaultSections(),
                                        subjects: getSubjectsByGrade(i + 1),
                                    })
                                }
                                disabled={watchForm.grades.some((g) => g.grade === `Grade ${(i + 1)}`)}
                            >
                                <Plus className="h-4 w-4 mr-1" />
                                Grade {i + 1}
                            </Button>
                        ))}
                    </div>
                </div>

                {/* Custom Grade */}
                <div className="mb-6">
                    <Button variant="outline">
                        <Plus className="h-4 w-4 mr-2" />
                        Add Custom Grade
                    </Button>
                </div>

                {/* Grades List */}
                <div className="space-y-4">
                    {watchForm.grades.map((grade, index) => (
                        <GradeCard
                            key={index}
                            form={form}
                            index={index}
                        />
                    ))}
                </div>
            </CardContent>

        </Card>
    )
}

interface GradeCardProps {
    form: UseFormReturn<YearSetupType>
    index: number
}

interface StreamsManagementProps {
    form: UseFormReturn<YearSetupType>
    formIndex: number
}

function StreamsManagement({ form, formIndex }: StreamsManagementProps) {
    const [isOpen, setIsOpen] = useState(false)
    const { fields: streamFields, append: appendStream, prepend: prependStream, remove: removeStream } = useFieldArray({
        control: form.control,
        name: `grades.${formIndex}.streams`,
    })
    const watchForm = form.watch()

    const handleSave = () => {
        toast.success("New Stream Added To the List", {
            style: { color: "green" },
        });
        setIsOpen(false);
    };

    const handleCancel = () => {
        removeStream(0);
        setIsOpen(false);
    };


    return (
        <div className="space-y-4">
            <div className="flex items-center gap-2">
                <Layers className="h-4 w-4" />
                <Label>Academic Streams</Label>
            </div>
            <div className="flex flex-wrap gap-2">
                {["Natural Science", "Social Science"].map((stream, streamIndex) => (
                    <Button
                        key={streamIndex}
                        variant="outline"
                        size="sm"
                        onClick={() => appendStream({
                            id: "",
                            gradeId: "",
                            name: stream,
                            subjects: [],
                        })}
                        disabled={watchForm.grades[formIndex].streams.some((s) => s.name === stream)}
                    >
                        <Plus className="h-4 w-4 mr-1" />
                        {stream}
                    </Button>
                ))}
                {/* Add Custom Stream */}
                <Dialog open={isOpen} onOpenChange={setIsOpen}>
                    <DialogTrigger asChild>
                        <Button variant="outline" size="sm" className="text-sm" onClick={() => prependStream({ id: "", gradeId: "", name: "", subjects: [] })}>
                            <Plus className="h-4 w-4 mr-1" />
                            Custom stream name
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <div className="relative">
                            <DialogHeader>
                                <DialogTitle>Custom Stream Name</DialogTitle>
                                <DialogDescription>
                                    Enter a name for the custom stream you want to create.
                                </DialogDescription>
                            </DialogHeader>
                        </div>
                        <div>
                            <InputWithLabel
                                fieldTitle="Enter stream name *"
                                nameInSchema={`grades.${formIndex}.streams.${0}.name`}
                                placeholder="e.g., Art"
                            />
                        </div>
                        <DialogFooter>
                            <Button className="mt-0" variant="outline" onClick={() => handleCancel()}>Cancel</Button>
                            <Button onClick={() => handleSave()}>Add Stream</Button>
                        </DialogFooter>
                    </DialogContent>
                </Dialog>
            </div>
            {/* Stream List */}
            <div className="space-y-3">
                {watchForm.grades[formIndex].streams.map((stream, streamIndex) => (
                    <Card key={stream.id} className="p-4">
                        <div className="flex items-start justify-between mb-3">
                            <div>
                                <h4 className="font-medium">{stream.name}</h4>
                            </div>
                            <Button variant="outline" size="sm"
                                onClick={() => removeStream(streamIndex)} className="ml-2"
                            >
                                <X className="h-4 w-4" />
                            </Button>
                        </div>
                        <div className="mt-3">
                            <Label className="text-sm">Stream Subjects</Label>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {watchForm.grades[formIndex].streams[streamIndex].subjects.length === 0 && (
                                    <Badge variant="outline" className="text-sm">
                                        No subjects added yet
                                    </Badge>
                                )}
                            </div>
                        </div>
                    </Card>
                ))}
            </div>
        </div>

    );
}


function GradeCard({ form, index }: GradeCardProps) {
    const [isCollapsed, setIsCollapsed] = useState(true)

    const { fields: gradeFields, append: appendGrade, remove: removeGrade, } = useFieldArray({
        control: form.control,
        name: "grades",
    })
    const { fields: subjectFields, append: appendSubject, remove: removeSubject } = useFieldArray({
        control: form.control,
        name: `grades.${index}.subjects`,
    })
    const { fields: sectionFields, append: appendSection, remove: removeSection } = useFieldArray({
        control: form.control,
        name: `grades.${index}.sections`,
    })
    const { fields: streamFields, append: appendStream, remove: removeStream } = useFieldArray({
        control: form.control,
        name: `grades.${index}.streams`,
    })

    const watchForm = form.watch()

    const generateSections = (maxSections: number) => {
        const sections = []
        for (let i = 0; i < maxSections; i++) {
            sections.push(String.fromCharCode(65 + i)) // A, B, C, D...
        }
        return sections
    }

    const getSectionObjects = (index: string) => {
        const sectionCount = parseInt(index, 10);

        if (isNaN(sectionCount) || sectionCount < 1 || sectionCount > 26) {
            console.error("Invalid section count. Must be a number between 1 and 26.");
            return [];
        }

        return Array.from({ length: sectionCount }, (_, i) => ({
            id: crypto.randomUUID(),
            gradeId: "",
            section: String.fromCharCode(65 + i), // A, B, C, D...
        }))
    }


    return (
        <Card className="w-full transition-all duration-300">
            <CardHeader
                className="flex flex-row items-center justify-between space-y-0 pb-4 cursor-pointer"
                onClick={() => setIsCollapsed(!isCollapsed)}
            >
                <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        {watchForm.grades[index].grade}
                    </CardTitle>
                    {isCollapsed && (
                        <div className="mt-2">
                            {/* <GradeSummary /> */}
                        </div>
                    )}
                </div>
                <div className="flex items-center gap-2">
                    <Button variant="ghost" size="sm" onClick={() => removeGrade(index)}>
                        <X className="h-4 w-4" />
                    </Button>
                    <ChevronDown
                        className={`h-5 w-5 transition-transform duration-300 ${!isCollapsed ? "rotate-180" : ""}`} />
                </div>
            </CardHeader>
            {!isCollapsed && (
                <CardContent className="space-y-6 pt-4 border-t">
                    {/* Sections */}
                    <SelectForObject<YearSetupType["grades"][number]["sections"]>
                        fieldTitle="Sections"
                        nameInSchema={`grades.${index}.sections`}
                        getObjects={(index) => getSectionObjects(index)}
                    >
                        {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                            <SelectItem key={num} value={num.toString()}>
                                {num} Section{num > 1 ? "s" : ""} ({generateSections(num).join(", ")})
                            </SelectItem>
                        ))}
                    </SelectForObject>
                    <div className="flex gap-1 mt-2">
                        {watchForm.grades[index].sections.map((section) => (
                            <Badge key={section.id} variant="outline">
                                Section {section.section}
                            </Badge>
                        ))}
                    </div>
                    {/* Streams Toggle */}
                    <div className="flex items-center justify-between">
                        <div>
                            <Label>Has Streams/Tracks</Label>
                            <p className="text-sm text-gray-500">Enable different academic tracks for this grade</p>
                        </div>
                        <SwitchWithLabel
                            fieldTitle=""
                            nameInSchema={`grades.${index}.hasStream`} />
                    </div>
                    {/* Streams Management */}
                    {watchForm.grades[index].hasStream && (
                        <StreamsManagement form={form} formIndex={index} />
                    )}
                    {/* Grade Subjects (for non-stream grades) */}
                    {!watchForm.grades[index].hasStream && (
                        <div>
                            <Label>Grade Subjects</Label>
                            <p className="text-sm text-gray-500 mb-3">Selected subjects for this grade</p>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {watchForm.subjects.map((subject, subjectIndex) => (
                                    <div key={subject.id} className="flex items-center space-x-2">
                                        <CheckboxForObject<Subject>
                                            fieldTitle={subject.name}
                                            nameInSchema={`grades.${index}.subjects`}
                                            value={subject}
                                            className="w-4 h-4" />
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                    {/* Grade Summary */}
                    <div className="bg-gray-50 p-3 rounded-lg">
                        <h3 className="font-medium mb-2">Configuration Summary</h3>
                        {/* <GradeSummary /> */}
                    </div>
                </CardContent>
            )}
        </Card>
    )
}
