"use client"

import { useState, useEffect } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { X, BookOpen, GraduationCap } from "lucide-react"
import type { SubjectWithAssignments, SubjectFormData, GradeWithStreams } from "../types/subject-management"

interface SubjectFormDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
    subject?: SubjectWithAssignments
    grades: GradeWithStreams[]
    onSave: (data: SubjectFormData) => void
    mode: "create" | "edit"
}

export function SubjectFormDialog({ open, onOpenChange, subject, grades, onSave, mode }: SubjectFormDialogProps) {
    const [formData, setFormData] = useState<SubjectFormData>({
        name: "",
        code: "",
        category: "core",
        description: "",
        isRequired: false,
        assignments: [],
    })

    const [errors, setErrors] = useState<Record<string, string>>({})

    useEffect(() => {
        if (subject && mode === "edit") {
            setFormData({
                name: subject.name,
                code: subject.code,
                category: subject.category,
                description: subject.description,
                isRequired: subject.isRequired,
                assignments: subject.assignments.map((assignment) => ({
                    gradeId: assignment.gradeId,
                    streamId: assignment.streamId,
                    isRequired: assignment.isRequired,
                })),
            })
        } else {
            setFormData({
                name: "",
                code: "",
                category: "core",
                description: "",
                isRequired: false,
                assignments: [],
            })
        }
        setErrors({})
    }, [subject, mode, open])

    const validateForm = () => {
        const newErrors: Record<string, string> = {}

        if (!formData.name.trim()) {
            newErrors.name = "Subject name is required"
        }

        if (!formData.code.trim()) {
            newErrors.code = "Subject code is required"
        } else if (formData.code.length < 2) {
            newErrors.code = "Subject code must be at least 2 characters"
        }

        if (!formData.description.trim()) {
            newErrors.description = "Description is required"
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    const handleSave = () => {
        if (validateForm()) {
            onSave(formData)
            onOpenChange(false)
        }
    }

    const addAssignment = (gradeId: string, streamId?: string) => {
        const existingIndex = formData.assignments.findIndex((a) => a.gradeId === gradeId && a.streamId === streamId)

        if (existingIndex === -1) {
            setFormData({
                ...formData,
                assignments: [
                    ...formData.assignments,
                    {
                        gradeId,
                        streamId,
                        isRequired: false,
                    },
                ],
            })
        }
    }

    const removeAssignment = (gradeId: string, streamId?: string) => {
        setFormData({
            ...formData,
            assignments: formData.assignments.filter((a) => !(a.gradeId === gradeId && a.streamId === streamId)),
        })
    }

    const updateAssignmentRequired = (gradeId: string, streamId: string | undefined, isRequired: boolean) => {
        setFormData({
            ...formData,
            assignments: formData.assignments.map((a) =>
                a.gradeId === gradeId && a.streamId === streamId ? { ...a, isRequired } : a,
            ),
        })
    }

    const isAssigned = (gradeId: string, streamId?: string) => {
        return formData.assignments.some((a) => a.gradeId === gradeId && a.streamId === streamId)
    }

    const getAssignmentRequired = (gradeId: string, streamId?: string) => {
        const assignment = formData.assignments.find((a) => a.gradeId === gradeId && a.streamId === streamId)
        return assignment?.isRequired || false
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
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        {mode === "create" ? "Create New Subject" : "Edit Subject"}
                    </DialogTitle>
                </DialogHeader>

                <div className="space-y-6">
                    {/* Basic Information */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="text-lg">Basic Information</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="name">Subject Name *</Label>
                                    <Input
                                        id="name"
                                        value={formData.name}
                                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                        placeholder="e.g., Advanced Mathematics"
                                        className={errors.name ? "border-red-500" : ""}
                                    />
                                    {errors.name && <p className="text-sm text-red-500 mt-1">{errors.name}</p>}
                                </div>

                                <div>
                                    <Label htmlFor="code">Subject Code *</Label>
                                    <Input
                                        id="code"
                                        value={formData.code}
                                        onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                                        placeholder="e.g., MATH"
                                        className={errors.code ? "border-red-500" : ""}
                                    />
                                    {errors.code && <p className="text-sm text-red-500 mt-1">{errors.code}</p>}
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="category">Category</Label>
                                <Select
                                    value={formData.category}
                                    onValueChange={(value: any) => setFormData({ ...formData, category: value })}
                                >
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="core">Core Subject</SelectItem>
                                        <SelectItem value="language">Language</SelectItem>
                                        <SelectItem value="arts">Arts & Creative</SelectItem>
                                        <SelectItem value="physical">Physical Education</SelectItem>
                                        <SelectItem value="technical">Technical & Vocational</SelectItem>
                                        <SelectItem value="elective">Elective</SelectItem>
                                    </SelectContent>
                                </Select>
                                <div className="mt-2">
                                    <Badge className={`text-xs ${getCategoryColor(formData.category)}`}>{formData.category}</Badge>
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="description">Description *</Label>
                                <Textarea
                                    id="description"
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    placeholder="Brief description of the subject..."
                                    rows={3}
                                    className={errors.description ? "border-red-500" : ""}
                                />
                                {errors.description && <p className="text-sm text-red-500 mt-1">{errors.description}</p>}
                            </div>

                            <div className="flex items-center space-x-2">
                                <Switch
                                    checked={formData.isRequired}
                                    onCheckedChange={(checked) => setFormData({ ...formData, isRequired: checked })}
                                />
                                <Label>Required Subject (applies to all assignments)</Label>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Grade and Stream Assignments */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <GraduationCap className="h-5 w-5" />
                                Grade & Stream Assignments
                            </CardTitle>
                            <p className="text-sm text-gray-600">Select which grades and streams this subject will be taught in</p>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {grades.map((grade) => (
                                    <Card key={grade.id} className="p-4">
                                        <div className="flex items-center justify-between mb-3">
                                            <h4 className="font-medium">{grade.name}</h4>
                                            <Badge variant="outline">Level {grade.level}</Badge>
                                        </div>

                                        {grade.hasStreams && grade.streams.length > 0 ? (
                                            // Grade with streams
                                            <div className="space-y-2">
                                                <Label className="text-sm text-gray-600">Streams:</Label>
                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                                                    {grade.streams.map((stream) => (
                                                        <div
                                                            key={stream.id}
                                                            className={`border rounded-lg p-3 transition-colors ${isAssigned(grade.id, stream.id)
                                                                ? "border-blue-500 bg-blue-50"
                                                                : "border-gray-200 hover:border-gray-300"
                                                                }`}
                                                        >
                                                            <div className="flex items-center justify-between mb-2">
                                                                <div className="flex items-center space-x-2">
                                                                    <Checkbox
                                                                        checked={isAssigned(grade.id, stream.id)}
                                                                        onCheckedChange={(checked) => {
                                                                            if (checked) {
                                                                                addAssignment(grade.id, stream.id)
                                                                            } else {
                                                                                removeAssignment(grade.id, stream.id)
                                                                            }
                                                                        }}
                                                                    />
                                                                    <div>
                                                                        <p className="font-medium text-sm">{stream.name}</p>
                                                                        <p className="text-xs text-gray-500">{stream.code}</p>
                                                                    </div>
                                                                </div>
                                                                {isAssigned(grade.id, stream.id) && (
                                                                    <div className="flex items-center space-x-2">
                                                                        <Switch
                                                                            checked={getAssignmentRequired(grade.id, stream.id)}
                                                                            onCheckedChange={(checked) =>
                                                                                updateAssignmentRequired(grade.id, stream.id, checked)
                                                                            }
                                                                            size="sm"
                                                                        />
                                                                        <Label className="text-xs">Required</Label>
                                                                    </div>
                                                                )}
                                                            </div>
                                                            {stream.description && <p className="text-xs text-gray-600">{stream.description}</p>}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        ) : (
                                            // Grade without streams
                                            <div
                                                className={`border rounded-lg p-3 transition-colors ${isAssigned(grade.id) ? "border-blue-500 bg-blue-50" : "border-gray-200 hover:border-gray-300"
                                                    }`}
                                            >
                                                <div className="flex items-center justify-between">
                                                    <div className="flex items-center space-x-2">
                                                        <Checkbox
                                                            checked={isAssigned(grade.id)}
                                                            onCheckedChange={(checked) => {
                                                                if (checked) {
                                                                    addAssignment(grade.id)
                                                                } else {
                                                                    removeAssignment(grade.id)
                                                                }
                                                            }}
                                                        />
                                                        <Label>Assign to {grade.name}</Label>
                                                    </div>
                                                    {isAssigned(grade.id) && (
                                                        <div className="flex items-center space-x-2">
                                                            <Switch
                                                                checked={getAssignmentRequired(grade.id, undefined)}
                                                                onCheckedChange={(checked) => updateAssignmentRequired(grade.id, undefined, checked)}
                                                                size="sm"
                                                            />
                                                            <Label className="text-xs">Required</Label>
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        )}
                                    </Card>
                                ))}
                            </div>

                            {/* Assignment Summary */}
                            {formData.assignments.length > 0 && (
                                <Card className="mt-4 bg-blue-50 border-blue-200">
                                    <CardContent className="p-4">
                                        <h4 className="font-medium mb-2">Assignment Summary</h4>
                                        <div className="flex flex-wrap gap-2">
                                            {formData.assignments.map((assignment, index) => {
                                                const grade = grades.find((g) => g.id === assignment.gradeId)
                                                const stream = assignment.streamId
                                                    ? grade?.streams.find((s) => s.id === assignment.streamId)
                                                    : null

                                                return (
                                                    <Badge
                                                        key={index}
                                                        variant={assignment.isRequired ? "default" : "secondary"}
                                                        className="flex items-center gap-1"
                                                    >
                                                        {grade?.name}
                                                        {stream && ` - ${stream.name}`}
                                                        {assignment.isRequired && <span className="text-xs">*</span>}
                                                        <button
                                                            onClick={() => removeAssignment(assignment.gradeId, assignment.streamId)}
                                                            className="ml-1 hover:bg-red-500 hover:text-white rounded-full p-0.5"
                                                        >
                                                            <X className="h-3 w-3" />
                                                        </button>
                                                    </Badge>
                                                )
                                            })}
                                        </div>
                                    </CardContent>
                                </Card>
                            )}
                        </CardContent>
                    </Card>

                    {/* Action Buttons */}
                    <div className="flex justify-end gap-3">
                        <Button variant="outline" onClick={() => onOpenChange(false)}>
                            Cancel
                        </Button>
                        <Button onClick={handleSave}>{mode === "create" ? "Create Subject" : "Update Subject"}</Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    )
}
