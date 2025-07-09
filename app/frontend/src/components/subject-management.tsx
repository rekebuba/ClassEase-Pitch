"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { Plus, X, BookOpen, Filter } from "lucide-react"
import type { Subject } from "@/lib/academic-year"
import { SUGGESTED_SUBJECTS } from "@/lib/academic-year"

interface SubjectManagementProps {
    subjects: Subject[]
    onUpdate: (subjects: Subject[]) => void
}

export default function SubjectManagement({ subjects, onUpdate }: SubjectManagementProps) {
    const [selectedCategory, setSelectedCategory] = useState<string>("all")
    const [newSubject, setNewSubject] = useState<Partial<Subject>>({
        name: "",
        code: "",
        category: "core",
        description: "",
        isRequired: false,
    })

    const addSuggestedSubject = (suggestedSubject: Subject) => {
        if (!subjects.find((s) => s.id === suggestedSubject.id)) {
            onUpdate([...subjects, { ...suggestedSubject, grades: [] }])
        }
    }

    const addCustomSubject = () => {
        if (newSubject.name && newSubject.code) {
            const subject: Subject = {
                id: Date.now().toString(),
                name: newSubject.name,
                code: newSubject.code.toUpperCase(),
                category: newSubject.category as Subject["category"],
                description: newSubject.description || "",
                grades: [],
                isRequired: newSubject.isRequired || false,
            }
            onUpdate([...subjects, subject])
            setNewSubject({
                name: "",
                code: "",
                category: "core",
                description: "",
                isRequired: false,
            })
        }
    }

    const removeSubject = (subjectId: string) => {
        onUpdate(subjects.filter((s) => s.id !== subjectId))
    }

    const updateSubject = (subjectId: string, updates: Partial<Subject>) => {
        onUpdate(subjects.map((s) => (s.id === subjectId ? { ...s, ...updates } : s)))
    }

    const filteredSuggestions =
        selectedCategory === "all" ? SUGGESTED_SUBJECTS : SUGGESTED_SUBJECTS.filter((s) => s.category === selectedCategory)

    const getCategoryColor = (category: Subject["category"]) => {
        const colors = {
            core: "bg-blue-100 text-blue-800",
            elective: "bg-green-100 text-green-800",
            language: "bg-purple-100 text-purple-800",
            arts: "bg-pink-100 text-pink-800",
            physical: "bg-orange-100 text-orange-800",
            technical: "bg-gray-100 text-gray-800",
        }
        return colors[category] || colors.core
    }

    return (
        <div className="space-y-6">
            {/* Subject Suggestions */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        Subject Library
                    </CardTitle>
                    <p className="text-sm text-gray-600">Add subjects from our curated library</p>
                </CardHeader>
                <CardContent className="space-y-4">
                    {/* Category Filter */}
                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4" />
                        <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                            <SelectTrigger className="w-48">
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Categories</SelectItem>
                                <SelectItem value="core">Core Subjects</SelectItem>
                                <SelectItem value="language">Languages</SelectItem>
                                <SelectItem value="arts">Arts & Creative</SelectItem>
                                <SelectItem value="physical">Physical Education</SelectItem>
                                <SelectItem value="technical">Technical & Vocational</SelectItem>
                                <SelectItem value="elective">Electives</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Suggested Subjects Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {filteredSuggestions.map((subject) => {
                            const isAdded = subjects.find((s) => s.id === subject.id)
                            return (
                                <Card
                                    key={subject.id}
                                    className={`p-3 cursor-pointer transition-colors ${isAdded ? "bg-green-50 border-green-200" : "hover:bg-gray-50"}`}
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2 mb-1">
                                                <h4 className="font-medium text-sm">{subject.name}</h4>
                                                <Badge className={`text-xs ${getCategoryColor(subject.category)}`}>{subject.category}</Badge>
                                            </div>
                                            <p className="text-xs text-gray-500 mb-2">{subject.description}</p>
                                            <div className="flex items-center gap-2">
                                                <Badge variant="outline" className="text-xs">
                                                    {subject.code}
                                                </Badge>
                                                {subject.isRequired && (
                                                    <Badge variant="destructive" className="text-xs">
                                                        Required
                                                    </Badge>
                                                )}
                                            </div>
                                        </div>
                                        <Button
                                            size="sm"
                                            variant={isAdded ? "outline" : "default"}
                                            onClick={() => addSuggestedSubject(subject)}
                                            disabled={!!isAdded}
                                        >
                                            {isAdded ? "Added" : <Plus className="h-4 w-4" />}
                                        </Button>
                                    </div>
                                </Card>
                            )
                        })}
                    </div>
                </CardContent>
            </Card>

            {/* Add Custom Subject */}
            <Card>
                <CardHeader>
                    <CardTitle>Add Custom Subject</CardTitle>
                    <p className="text-sm text-gray-600">Create a custom subject not in our library</p>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <Label>Subject Name</Label>
                            <Input
                                value={newSubject.name || ""}
                                onChange={(e) => setNewSubject({ ...newSubject, name: e.target.value })}
                                placeholder="e.g., Advanced Calculus"
                            />
                        </div>
                        <div>
                            <Label>Subject Code</Label>
                            <Input
                                value={newSubject.code || ""}
                                onChange={(e) => setNewSubject({ ...newSubject, code: e.target.value.toUpperCase() })}
                                placeholder="e.g., CALC"
                            />
                        </div>
                        <div>
                            <Label>Category</Label>
                            <Select
                                value={newSubject.category}
                                onValueChange={(value) => setNewSubject({ ...newSubject, category: value as Subject["category"] })}
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
                        </div>
                        <div className="flex items-center space-x-2">
                            <Switch
                                checked={newSubject.isRequired || false}
                                onCheckedChange={(checked) => setNewSubject({ ...newSubject, isRequired: checked })}
                            />
                            <Label>Required Subject</Label>
                        </div>
                        <div className="md:col-span-2">
                            <Label>Description</Label>
                            <Textarea
                                value={newSubject.description || ""}
                                onChange={(e) => setNewSubject({ ...newSubject, description: e.target.value })}
                                placeholder="Brief description of the subject..."
                                rows={2}
                            />
                        </div>
                        <div className="md:col-span-2">
                            <Button onClick={addCustomSubject} className="w-full">
                                <Plus className="h-4 w-4 mr-2" />
                                Add Custom Subject
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Selected Subjects */}
            <Card>
                <CardHeader>
                    <CardTitle>Selected Subjects ({subjects.length})</CardTitle>
                    <p className="text-sm text-gray-600">Subjects that will be available for this academic year</p>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                        {subjects.map((subject) => (
                            <Card key={subject.id} className="p-3">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-1">
                                            <h4 className="font-medium text-sm">{subject.name}</h4>
                                            <Badge className={`text-xs ${getCategoryColor(subject.category)}`}>{subject.category}</Badge>
                                        </div>
                                        <p className="text-xs text-gray-500 mb-2">{subject.description}</p>
                                        <div className="flex items-center gap-2">
                                            <Badge variant="outline" className="text-xs">
                                                {subject.code}
                                            </Badge>
                                            {subject.isRequired && (
                                                <Badge variant="destructive" className="text-xs">
                                                    Required
                                                </Badge>
                                            )}
                                        </div>
                                    </div>
                                    <Button size="sm" variant="outline" onClick={() => removeSubject(subject.id)}>
                                        <X className="h-4 w-4" />
                                    </Button>
                                </div>
                            </Card>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
