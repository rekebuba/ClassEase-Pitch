"use client"

import { useMemo, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
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
import { Plus, X, BookOpen, Filter, CheckCircle, Edit, Trash2, GraduationCap, Users, MoreHorizontal, Eye } from "lucide-react"
import type { Subject } from "@/lib/academic-year"
import { GradeLevelEnum } from "@/lib/enums"
import { SubjectCard } from "./subject-card"
import { SubjectFormDialog } from "./subject-form-dialog"
import { SubjectDetailDialog } from "./subject-detail-dialog"

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
    const [searchTerm, setSearchTerm] = useState("")
    const [categoryFilter, setCategoryFilter] = useState<string>("all")
    const [gradeFilter, setGradeFilter] = useState<string>("all")
    const [formDialogOpen, setFormDialogOpen] = useState(false)
    const [detailDialogOpen, setDetailDialogOpen] = useState(false)
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
    const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null)
    const [formMode, setFormMode] = useState<"create" | "edit">("create")


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

    const handleCreate = () => {
        setSelectedSubject(null)
        setFormMode("create")
        setFormDialogOpen(true)
    }

    const handleEdit = (subject: Subject) => {
        setSelectedSubject(subject)
        setFormMode("edit")
        setFormDialogOpen(true)
    }

    const handleView = (subject: Subject) => {
        setSelectedSubject(subject)
        setDetailDialogOpen(true)
    }

    const handleDelete = (subject: Subject) => {
        setSelectedSubject(subject)
        setDeleteDialogOpen(true)
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
                            return (
                                <SubjectCard
                                    key={subject.id}
                                    subject={subject}
                                    grades={subject.grades}
                                    onEdit={() => handleEdit(subject)}
                                    onDelete={() => handleDelete(subject)}
                                    onView={() => handleView(subject)}
                                />
                            )
                        })}
                    </div>
                </CardContent>
            </Card>

            {/* Dialogs */}
            <SubjectFormDialog
                open={formDialogOpen}
                onOpenChange={setFormDialogOpen}
                subject={selectedSubject}
                grades={subject.grade}
                onSave={handleSave}
                mode={formMode}
            />

            <SubjectDetailDialog
                open={detailDialogOpen}
                onOpenChange={setDetailDialogOpen}
                subject={selectedSubject}
                grades={mockGrades}
                onEdit={() => {
                    setDetailDialogOpen(false)
                    handleEdit(selectedSubject!)
                }}
            />

            {/* Add Subject Dialog */}
            {/* <AlertDialog open={isAddingSubject} onOpenChange={setIsAddingSubject}>
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
            </AlertDialog> */}

            {/* Edit Subject Dialog */}
            {/* <AlertDialog open={!!editingSubject} onOpenChange={(isOpen) => !isOpen && setEditingSubject(null)}>
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
            </AlertDialog> */}
        </div>
    )
}
