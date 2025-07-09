"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Switch } from "@/components/ui/switch"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Plus, X, Users, BookOpen, Layers } from "lucide-react"
import type { Grade, Stream } from "@/lib/academic-year"
import { STREAM_SUGGESTIONS } from "@/lib/academic-year"

interface GradeSetupCardProps {
    grade: Grade
    onUpdate: (grade: Grade) => void
    onRemove: () => void
    availableSubjects: string[]
}

export default function GradeSetupCard({ grade, onUpdate, onRemove, availableSubjects }: GradeSetupCardProps) {
    const [newStreamName, setNewStreamName] = useState("")
    const [selectedStreamSuggestion, setSelectedStreamSuggestion] = useState("")

    const updateGrade = (updates: Partial<Grade>) => {
        onUpdate({ ...grade, ...updates })
    }

    const addStream = () => {
        if (selectedStreamSuggestion) {
            const suggestion = STREAM_SUGGESTIONS.find((s) => s.code === selectedStreamSuggestion)
            if (suggestion) {
                const newStream: Stream = {
                    id: Date.now().toString(),
                    name: suggestion.name,
                    code: suggestion.code,
                    description: suggestion.description,
                    subjects: suggestion.subjects.filter((s) => availableSubjects.includes(s)),
                }
                updateGrade({ streams: [...grade.streams, newStream] })
                setSelectedStreamSuggestion("")
            }
        } else if (newStreamName.trim()) {
            const newStream: Stream = {
                id: Date.now().toString(),
                name: newStreamName.trim(),
                code: newStreamName.trim().toUpperCase().replace(/\s+/g, ""),
                description: "",
                subjects: [],
            }
            updateGrade({ streams: [...grade.streams, newStream] })
            setNewStreamName("")
        }
    }

    const removeStream = (streamId: string) => {
        updateGrade({ streams: grade.streams.filter((s) => s.id !== streamId) })
    }

    const updateStream = (streamId: string, updates: Partial<Stream>) => {
        updateGrade({
            streams: grade.streams.map((s) => (s.id === streamId ? { ...s, ...updates } : s)),
        })
    }

    const generateSections = (maxSections: number) => {
        const sections = []
        for (let i = 0; i < maxSections; i++) {
            sections.push(String.fromCharCode(65 + i)) // A, B, C, D...
        }
        return sections
    }

    const toggleSubject = (subject: string) => {
        const currentSubjects = grade.subjects || []
        const updatedSubjects = currentSubjects.includes(subject)
            ? currentSubjects.filter((s) => s !== subject)
            : [...currentSubjects, subject]
        updateGrade({ subjects: updatedSubjects })
    }

    return (
        <Card className="w-full">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <CardTitle className="flex items-center gap-2">
                    <BookOpen className="h-5 w-5" />
                    {grade.name}
                </CardTitle>
                <Button variant="outline" size="sm" onClick={onRemove}>
                    <X className="h-4 w-4" />
                </Button>
            </CardHeader>
            <CardContent className="space-y-6">
                {/* Basic Grade Info */}
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <Label htmlFor={`grade-${grade.id}-name`}>Grade Name</Label>
                        <Input
                            id={`grade-${grade.id}-name`}
                            value={grade.name}
                            onChange={(e) => updateGrade({ name: e.target.value })}
                            placeholder="e.g., Grade 10"
                        />
                    </div>
                    <div>
                        <Label htmlFor={`grade-${grade.id}-level`}>Grade Level</Label>
                        <Input
                            id={`grade-${grade.id}-level`}
                            type="number"
                            value={grade.level}
                            onChange={(e) => updateGrade({ level: Number.parseInt(e.target.value) || 0 })}
                            placeholder="10"
                        />
                    </div>
                </div>

                {/* Sections */}
                <div>
                    <Label htmlFor={`grade-${grade.id}-sections`}>Maximum Sections</Label>
                    <Select
                        value={grade.maxSections.toString()}
                        onValueChange={(value) => {
                            const maxSections = Number.parseInt(value)
                            updateGrade({
                                maxSections,
                                sections: generateSections(maxSections),
                            })
                        }}
                    >
                        <SelectTrigger>
                            <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                            {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                                <SelectItem key={num} value={num.toString()}>
                                    {num} Section{num > 1 ? "s" : ""} ({generateSections(num).join(", ")})
                                </SelectItem>
                            ))}
                        </SelectContent>
                    </Select>
                    <div className="flex gap-1 mt-2">
                        {grade.sections.map((section) => (
                            <Badge key={section} variant="outline">
                                Section {section}
                            </Badge>
                        ))}
                    </div>
                </div>

                {/* Streams Toggle */}
                <div className="flex items-center justify-between">
                    <div>
                        <Label>Has Streams/Tracks</Label>
                        <p className="text-sm text-gray-500">Enable different academic tracks for this grade</p>
                    </div>
                    <Switch
                        checked={grade.hasStreams}
                        onCheckedChange={(checked) => updateGrade({ hasStreams: checked, streams: checked ? grade.streams : [] })}
                    />
                </div>

                {/* Streams Management */}
                {grade.hasStreams && (
                    <div className="space-y-4">
                        <div className="flex items-center gap-2">
                            <Layers className="h-4 w-4" />
                            <Label>Academic Streams</Label>
                        </div>

                        {/* Add Stream */}
                        <div className="flex gap-2">
                            <Select value={selectedStreamSuggestion} onValueChange={setSelectedStreamSuggestion}>
                                <SelectTrigger className="flex-1">
                                    <SelectValue placeholder="Choose from suggestions..." />
                                </SelectTrigger>
                                <SelectContent>
                                    {STREAM_SUGGESTIONS.map((stream) => (
                                        <SelectItem key={stream.code} value={stream.code}>
                                            {stream.name} - {stream.description}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            <span className="text-gray-500 self-center">or</span>
                            <Input
                                placeholder="Custom stream name"
                                value={newStreamName}
                                onChange={(e) => setNewStreamName(e.target.value)}
                                className="flex-1"
                            />
                            <Button onClick={addStream} size="sm">
                                <Plus className="h-4 w-4" />
                            </Button>
                        </div>

                        {/* Stream List */}
                        <div className="space-y-3">
                            {grade.streams.map((stream) => (
                                <Card key={stream.id} className="p-4">
                                    <div className="flex items-start justify-between mb-3">
                                        <div>
                                            <h4 className="font-medium">{stream.name}</h4>
                                            <p className="text-sm text-gray-500">{stream.description}</p>
                                        </div>
                                        <Button variant="outline" size="sm" onClick={() => removeStream(stream.id)}>
                                            <X className="h-4 w-4" />
                                        </Button>
                                    </div>

                                    <div>
                                        <Label className="text-sm">Stream Description</Label>
                                        <Textarea
                                            value={stream.description}
                                            onChange={(e) => updateStream(stream.id, { description: e.target.value })}
                                            placeholder="Describe this academic stream..."
                                            className="mt-1"
                                            rows={2}
                                        />
                                    </div>

                                    <div className="mt-3">
                                        <Label className="text-sm">Stream Subjects</Label>
                                        <div className="flex flex-wrap gap-2 mt-2">
                                            {availableSubjects.map((subject) => (
                                                <Badge
                                                    key={subject}
                                                    variant={stream.subjects.includes(subject) ? "default" : "outline"}
                                                    className="cursor-pointer"
                                                    onClick={() => {
                                                        const updatedSubjects = stream.subjects.includes(subject)
                                                            ? stream.subjects.filter((s) => s !== subject)
                                                            : [...stream.subjects, subject]
                                                        updateStream(stream.id, { subjects: updatedSubjects })
                                                    }}
                                                >
                                                    {subject}
                                                </Badge>
                                            ))}
                                        </div>
                                    </div>
                                </Card>
                            ))}
                        </div>
                    </div>
                )}

                {/* Grade Subjects (for non-stream grades) */}
                {!grade.hasStreams && (
                    <div>
                        <Label>Grade Subjects</Label>
                        <p className="text-sm text-gray-500 mb-3">Select subjects for this grade</p>
                        <div className="flex flex-wrap gap-2">
                            {availableSubjects.map((subject) => (
                                <Badge
                                    key={subject}
                                    variant={grade.subjects.includes(subject) ? "default" : "outline"}
                                    className="cursor-pointer"
                                    onClick={() => toggleSubject(subject)}
                                >
                                    {subject}
                                </Badge>
                            ))}
                        </div>
                    </div>
                )}

                {/* Grade Summary */}
                <div className="bg-gray-50 p-3 rounded-lg">
                    <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1">
                            <Users className="h-4 w-4" />
                            <span>{grade.sections.length} Sections</span>
                        </div>
                        {grade.hasStreams && (
                            <div className="flex items-center gap-1">
                                <Layers className="h-4 w-4" />
                                <span>{grade.streams.length} Streams</span>
                            </div>
                        )}
                        <div className="flex items-center gap-1">
                            <BookOpen className="h-4 w-4" />
                            <span>
                                {grade.hasStreams
                                    ? `${grade.streams.reduce((acc, stream) => acc + stream.subjects.length, 0)} Total Subjects`
                                    : `${grade.subjects.length} Subjects`}
                            </span>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    )
}
