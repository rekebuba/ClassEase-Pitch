"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
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
import { Plus, X, BookOpen, Layers, ChevronDown, GraduationCap } from "lucide-react"
import { YearSetupType } from "@/lib/api-response-type"
import { useFieldArray, UseFormReturn } from "react-hook-form"
import { SelectWithLabel } from "./inputs/select-labeled"
import { SwitchWithLabel } from "./inputs/switch-labeled"
import { CheckboxForObject } from "./inputs/checkbox-for-object"
import { getDefaultSections, getStreamsByGrade, getSubjectsByGrade, hasStreamByGrade } from "@/config/suggestion"
import { SelectForObject } from "./inputs/select-for-object"
import { toast } from "sonner"
import { InputWithLabel } from "./inputs/input-labeled"
import { GradeLevelEnum } from "@/lib/enums"

type Grade = YearSetupType["grades"] extends Array<infer G> ? G : never
type Subject = YearSetupType["subjects"] extends Array<infer G> ? G : never

interface GradeSetupCardProps {
    form: UseFormReturn<YearSetupType>
    open: boolean
    onOpenChange: (open: boolean) => void
    formIndex: number
    mode: "create" | "edit"
}

export default function GradeSetupCard({ form, open, onOpenChange, mode, formIndex }: GradeSetupCardProps) {
    const { fields: gradeFields, append: appendGrade, remove: removeGrade, } = useFieldArray({
        control: form.control,
        name: "grades",
    })
    const [defaultData, setDefaultData] = useState<Grade>();

    useEffect(() => {
        if (open && mode === "edit") {
            const gradeData = form.getValues().grades[formIndex];
            if (gradeData) {
                setDefaultData(JSON.parse(JSON.stringify(gradeData)));
            }
        }
    }, [open, formIndex, form, mode]);

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

    const handleSave = () => {
        if (mode === "create") {
            toast.success("New Subject Added To the List", {
                style: { color: "green" },
            });
        } else {
            toast.success("Subject updated successfully", {
                style: { color: "green" },
            });
        }
        onOpenChange(false);
    };


    const handleCancel = () => {
        if (mode === "create") {
            removeGrade(formIndex);
        } else {
            if (defaultData) {
                console.log("formIndex: ", formIndex)
                console.log("Resetting to default data:", defaultData);
                form.setValue(`grades.${formIndex}`, defaultData);
            }
        }
        onOpenChange(false);
    };

    return (
        <Dialog open={open} onOpenChange={handleCancel}>
            <DialogContent className="max-w-5xl flex flex-col max-h-[90vh]">
                <DialogHeader className="flex items-center justify-between border-b pb-4 text-lg font-semibold">
                    <div className="flex items-center gap-2">
                        <GraduationCap className="text-blue-600" />
                        <DialogTitle>Configure Grade</DialogTitle>
                    </div>
                    <DialogDescription>
                        {watchForm.grades?.[formIndex]?.grade
                            ? "Configure"
                            : "Create New"} grade level and academic tracks.
                    </DialogDescription>
                </DialogHeader>
                <div className="flex-grow overflow-y-auto space-y-4">
                    <Card className="w-full transition-all duration-300">
                        <CardContent className="space-y-6 pt-4 border-t">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {/* Grade Name */}
                                <InputWithLabel
                                    fieldTitle="Grade Name *"
                                    nameInSchema={`grades.${formIndex}.grade`}
                                    placeholder="e.g. Grade 1"
                                />
                                {/* Grade Level */}
                                <SelectWithLabel
                                    fieldTitle="Grade Level *"
                                    nameInSchema={`grades.${formIndex}.level`}
                                >
                                    {GradeLevelEnum.options.map((level) => (
                                        <SelectItem key={level} value={level}>
                                            {level}
                                        </SelectItem>
                                    ))}
                                </SelectWithLabel>
                            </div>

                            {/* Sections */}
                            <SelectForObject<YearSetupType["grades"][number]["sections"]>
                                fieldTitle="Sections *"
                                nameInSchema={`grades.${formIndex}.sections`}
                                getObjects={(index) => getSectionObjects(index)}
                            >
                                {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                                    <SelectItem key={num} value={num.toString()}>
                                        {num} Section{num > 1 ? "s" : ""} ({generateSections(num).join(", ")})
                                    </SelectItem>
                                ))}
                            </SelectForObject>
                            <div className="flex gap-1 mt-2">
                                {watchForm.grades[formIndex].sections.map((section) => (
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
                                    nameInSchema={`grades.${formIndex}.hasStream`} />
                            </div>
                            {/* Streams Management */}
                            {watchForm.grades[formIndex].hasStream && (
                                <StreamsManagement form={form} formIndex={formIndex} />
                            )}
                            {/* Grade Subjects (for non-stream grades) */}
                            {!watchForm.grades[formIndex].hasStream && (
                                <div>
                                    <Label>Grade Subjects</Label>
                                    <p className="text-sm text-gray-500 mb-3">Selected subjects for this grade</p>
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        {watchForm.subjects.map((subject, subjectIndex) => (
                                            <div key={subject.id} className="flex items-center space-x-2">
                                                <CheckboxForObject<Subject>
                                                    fieldTitle={subject.name}
                                                    nameInSchema={`grades.${formIndex}.subjects`}
                                                    value={watchForm.grades[formIndex].subjects.find((s) => s.name === subject.name) || subject}
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
                    </Card>
                </div>
                <DialogFooter className="sticky bottom-0 bg-white border-t p-4 z-10">
                    <div className="ml-auto flex gap-3">
                        <Button variant="outline" onClick={handleCancel}>
                            Cancel
                        </Button>
                        <Button onClick={handleSave}>
                            {mode === "create" ? "Create Grade" : "Save Changes"}
                        </Button>
                    </div>
                </DialogFooter>
            </DialogContent>
        </Dialog >
    )
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
                        <div className="flex items-start justify-between mb-1">
                            <div>
                                <h4 className="font-medium">{stream.name}</h4>
                            </div>
                            <Button variant="outline" size="sm"
                                onClick={() => removeStream(streamIndex)} className="ml-2"
                            >
                                <X className="h-4 w-4" />
                            </Button>
                        </div>
                        <div className="mb-4">
                            <Label className="text-sm">Stream Subjects</Label>
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {watchForm.subjects.map((subject, subjectIndex) => (
                                <div key={subject.id} className="flex items-center space-x-2">
                                    <CheckboxForObject<Subject>
                                        fieldTitle={subject.name}
                                        nameInSchema={`grades.${formIndex}.streams.${streamIndex}.subjects`}
                                        value={watchForm.grades[formIndex].streams[streamIndex].subjects.find((s) => s.name === subject.name) || subject}
                                        className="w-4 h-4" />
                                </div>
                            ))}
                        </div>
                    </Card>
                ))}
            </div>
        </div>

    );
}
