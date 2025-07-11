"use client"

import { useMemo, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
    AlertDialog,
    AlertDialogContent,
    AlertDialogHeader,
    AlertDialogFooter,
    AlertDialogTitle,
    AlertDialogDescription,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Checkbox } from "@/components/ui/checkbox"
import { Plus, X, BookOpen, Filter, CheckCircle, Edit } from "lucide-react"
import type { Subject } from "@/lib/academic-year"
import { GradeLevelEnum } from "@/lib/enums"

interface SubjectManagementProps {
    suggestedSubjects: Subject[]
    subjects: Subject[]
    onUpdate: (subjects: Subject[]) => void
}

export default function SubjectManagement({ suggestedSubjects, subjects, onUpdate }: SubjectManagementProps) {
    const [selectedCategory, setSelectedCategory] = useState<string>("all")
    const [newSubject, setNewSubject] = useState<Partial<Subject>>({
        name: "",
        grades: [],
    })
    const [editingSubject, setEditingSubject] = useState<Subject | null>(null)
    const [isAddingSubject, setIsAddingSubject] = useState(false)

    const filteredSuggestions = useMemo(() => {
        if (selectedCategory === "all") {
            return suggestedSubjects
        }
        return suggestedSubjects.filter((subject) =>
            subject.grades.some((category) => category === selectedCategory)
        )
    }, [selectedCategory, suggestedSubjects])

    const toggleSubject = (suggestedSubject: Subject) => {
        const isAdded = subjects.find((s) => s.id === suggestedSubject.id)
        if (isAdded) {
            onUpdate(subjects.filter((s) => s.id !== suggestedSubject.id))
        } else {
            onUpdate([...subjects, { ...suggestedSubject, grades: [] }])
        }
    }

    const addCustomSubject = () => {
        if (newSubject.name && newSubject.grades && newSubject.grades.length > 0) {
            const subject: Subject = {
                id: Date.now().toString(),
                name: newSubject.name,
                code: [""],
                grades: newSubject.grades ?? [],
            }
            onUpdate([...subjects, subject])
            setNewSubject({ name: "", grades: [] })
            setIsAddingSubject(false)
        }
    }

    const updateSubject = (subjectId: string, updates: Partial<Subject>) => {
        onUpdate(subjects.map((s) => (s.id === subjectId ? { ...s, ...updates } : s)))
    }

    const handleEditSubject = (subject: Subject) => {
        setEditingSubject(subject)
    }

    const handleSaveSubject = () => {
        if (editingSubject) {
            updateSubject(editingSubject.id, editingSubject)
            setEditingSubject(null)
        }
    }

    const handleGradeChange = (grade: string, isEditing: boolean) => {
        if (isEditing && editingSubject) {
            const newGrades = editingSubject.grades.includes(grade)
                ? editingSubject.grades.filter((g) => g !== grade)
                : [...editingSubject.grades, grade]
            setEditingSubject({ ...editingSubject, grades: newGrades })
        } else {
            const newGrades = (newSubject.grades ?? []).includes(grade)
                ? (newSubject.grades ?? []).filter((g) => g !== grade)
                : [...(newSubject.grades ?? []), grade]
            setNewSubject({ ...newSubject, grades: newGrades })
        }
    }

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        Subject Library ({subjects.length})
                    </CardTitle>
                    <p className="text-sm text-gray-600">Add subjects from our curated library</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4" />
                        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                            <SelectTrigger className="w-48">
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Categories</SelectItem>
                                <SelectItem value="1">Grade 1-4</SelectItem>
                                <SelectItem value="5">Grade 5-6</SelectItem>
                                <SelectItem value="7">Grade 7-8</SelectItem>
                                <SelectItem value="9">Grade 9-10</SelectItem>
                                <SelectItem value="11-natural">Grade 11-12 (Natural)</SelectItem>
                                <SelectItem value="12-social">Grade 11-12 (Social)</SelectItem>
                            </SelectContent>
                        </Select>
                        <Button className="ml-auto" variant="outline" onClick={() => setIsAddingSubject(true)}>
                            <Plus className="h-4 w-4 mr-2" />
                            Add Custom Subject
                        </Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {filteredSuggestions.map((subject) => {
                            const isAdded = subjects.find((s) => s.id === subject.id)
                            return (
                                <Card
                                    key={subject.id}
                                    className={`p-3 transition-colors relative ${isAdded ? "bg-green-50 border-green-200" : "hover:bg-gray-50"
                                        }`}
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <Badge className="text-xs bg-purple-100 text-purple-800">
                                                    <h4 className="font-medium text-sm">{subject.name}</h4>
                                                </Badge>
                                            </div>
                                        </div>
                                        <div className="flex gap-2">
                                            <Button
                                                size="sm"
                                                variant={isAdded ? "outline" : "default"}
                                                onClick={(e) => {
                                                    e.stopPropagation()
                                                    toggleSubject(subject)
                                                }}
                                            >
                                                {isAdded ? <X className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
                                            </Button>
                                            <Button
                                                size="sm"
                                                variant="outline"
                                                onClick={(e) => {
                                                    e.stopPropagation()
                                                    handleEditSubject(subject)
                                                }}
                                            >
                                                <Edit className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-2 flex-wrap mt-2">
                                        {subject.grades.map((grade) => (
                                            <Badge
                                                key={grade}
                                                variant="outline"
                                                className="text-xs bg-gray-100 text-gray-800"
                                            >
                                                Grade {grade}
                                            </Badge>
                                        ))}
                                    </div>
                                    {isAdded && (
                                        <div className="absolute bottom-2 right-2">
                                            <CheckCircle className="h-5 w-5 text-green-500" />
                                        </div>
                                    )}
                                </Card>
                            )
                        })}
                    </div>
                </CardContent>
            </Card>

            {/* Add Subject Dialog */}
            <AlertDialog open={isAddingSubject} onOpenChange={setIsAddingSubject}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Add Custom Subject</AlertDialogTitle>
                        <AlertDialogDescription>
                            Create a custom subject not in our library.
                        </AlertDialogDescription>
                    </AlertDialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label>Subject Name</Label>
                            <Input
                                value={newSubject.name || ""}
                                onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                                placeholder="e.g., Advanced Calculus"
                            />
                        </div>
                        <div>
                            <Label>Grades</Label>
                            <div className="grid grid-cols-4 gap-2">
                                {Array.from({ length: 12 }, (_, i) => i + 1).map((grade) => (
                                    <div key={grade} className="flex items-center">
                                        <Checkbox
                                            id={`new-grade-${grade}`}
                                            checked={(newSubject.grades ?? []).includes(grade.toString())}
                                            onCheckedChange={() => handleGradeChange(grade.toString(), false)}
                                            className="mr-2"
                                        />
                                        <Label htmlFor={`new-grade-${grade}`}>Grade {grade}</Label>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                    <AlertDialogFooter>
                        <Button variant="outline" onClick={() => setIsAddingSubject(false)}>
                            Cancel
                        </Button>
                        <Button onClick={addCustomSubject}>Add Subject</Button>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>

            {/* Edit Subject Dialog */}
            <AlertDialog open={!!editingSubject} onOpenChange={(isOpen) => !isOpen && setEditingSubject(null)}>
                <AlertDialogContent>
                    <AlertDialogHeader>
                        <AlertDialogTitle>Edit Subject</AlertDialogTitle>
                    </AlertDialogHeader>
                    {editingSubject && (
                        <div className="space-y-4">
                            <div>
                                <Label>Subject Name</Label>
                                <Input
                                    value={editingSubject.name}
                                    onChange={(e) =>
                                        setEditingSubject({
                                            ...editingSubject,
                                            name: e.target.value,
                                        })
                                    }
                                />
                            </div>
                            <div>
                                <Label>Grades</Label>
                                <div className="grid grid-cols-4 gap-2">
                                    {Array.from({ length: 12 }, (_, i) => i + 1).map((grade) => (
                                        <div key={grade} className="flex items-center">
                                            <Checkbox
                                                id={`edit-grade-${grade}`}
                                                checked={editingSubject.grades.includes(grade.toString())}
                                                onCheckedChange={() => handleGradeChange(grade.toString(), true)}
                                                className="mr-2"
                                            />
                                            <Label htmlFor={`edit-grade-${grade}`}>Grade {grade}</Label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                            <AlertDialogFooter>
                                <Button variant="outline" onClick={() => setEditingSubject(null)}>
                                    Cancel
                                </Button>
                                <Button onClick={handleSaveSubject}>Save</Button>
                            </AlertDialogFooter>
                        </div>
                    )}
                </AlertDialogContent>
            </AlertDialog>
        </div>
    )
}
