import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen, Edit, GraduationCap, Calendar, Users } from "lucide-react"
import type { SubjectWithAssignments, GradeWithStreams } from "../types/subject-management"

interface SubjectDetailDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
    subject: SubjectWithAssignments | null
    grades: GradeWithStreams[]
    onEdit: () => void
}

export function SubjectDetailDialog({ open, onOpenChange, subject, grades, onEdit }: SubjectDetailDialogProps) {
    if (!subject) return null

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

    const getAssignmentsByGrade = () => {
        const gradeMap = new Map()

        subject.assignments.forEach((assignment) => {
            const grade = grades.find((g) => g.id === assignment.gradeId)
            if (!grade) return

            if (!gradeMap.has(grade.id)) {
                gradeMap.set(grade.id, {
                    grade,
                    assignments: [],
                })
            }

            gradeMap.get(grade.id).assignments.push(assignment)
        })

        return Array.from(gradeMap.values())
    }

    const gradeAssignments = getAssignmentsByGrade()

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <div className="flex items-center justify-between">
                        <DialogTitle className="flex items-center gap-2">
                            <BookOpen className="h-5 w-5" />
                            {subject.name}
                        </DialogTitle>
                        <Button onClick={onEdit}>
                            <Edit className="h-4 w-4 mr-2" />
                            Edit Subject
                        </Button>
                    </div>
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
                                    <label className="text-sm font-medium text-gray-600">Subject Name</label>
                                    <p className="text-lg font-semibold">{subject.name}</p>
                                </div>
                                <div>
                                    <label className="text-sm font-medium text-gray-600">Subject Code</label>
                                    <p className="text-lg font-semibold">{subject.code}</p>
                                </div>
                            </div>

                            <div>
                                <label className="text-sm font-medium text-gray-600">Category</label>
                                <div className="mt-1">
                                    <Badge className={`${getCategoryColor(subject.category)}`}>{subject.category}</Badge>
                                </div>
                            </div>

                            <div>
                                <label className="text-sm font-medium text-gray-600">Description</label>
                                <p className="text-gray-900 mt-1">{subject.description}</p>
                            </div>

                            <div>
                                <label className="text-sm font-medium text-gray-600">Subject Type</label>
                                <div className="mt-1">
                                    <Badge variant={subject.isRequired ? "destructive" : "secondary"}>
                                        {subject.isRequired ? "Required Subject" : "Optional Subject"}
                                    </Badge>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Assignment Overview */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <GraduationCap className="h-5 w-5" />
                                Grade & Stream Assignments ({subject.assignments.length})
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            {gradeAssignments.length > 0 ? (
                                <div className="space-y-4">
                                    {gradeAssignments.map(({ grade, assignments }) => (
                                        <Card key={grade.id} className="p-4">
                                            <div className="flex items-center justify-between mb-3">
                                                <h4 className="font-semibold">{grade.name}</h4>
                                                <Badge variant="outline">Level {grade.level}</Badge>
                                            </div>

                                            <div className="space-y-2">
                                                {assignments.map((assignment, index) => {
                                                    const stream = assignment.streamId
                                                        ? grade.streams.find((s) => s.id === assignment.streamId)
                                                        : null

                                                    return (
                                                        <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                                                            <div className="flex items-center gap-2">
                                                                <Users className="h-4 w-4 text-gray-500" />
                                                                <span className="font-medium">{stream ? `${stream.name} Stream` : "All Sections"}</span>
                                                                {stream && (
                                                                    <Badge variant="outline" className="text-xs">
                                                                        {stream.code}
                                                                    </Badge>
                                                                )}
                                                            </div>
                                                            <div className="flex items-center gap-2">
                                                                <Badge
                                                                    variant={assignment.isRequired ? "destructive" : "secondary"}
                                                                    className="text-xs"
                                                                >
                                                                    {assignment.isRequired ? "Required" : "Optional"}
                                                                </Badge>
                                                            </div>
                                                        </div>
                                                    )
                                                })}
                                            </div>
                                        </Card>
                                    ))}
                                </div>
                            ) : (
                                <div className="text-center py-8 text-gray-500">
                                    <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                    <p>This subject is not assigned to any grades yet.</p>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Assignment Summary */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Assignment Summary</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="text-center p-4 bg-blue-50 rounded-lg">
                                    <GraduationCap className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                                    <div className="text-2xl font-bold text-blue-900">
                                        {new Set(subject.assignments.map((a) => a.gradeId)).size}
                                    </div>
                                    <div className="text-sm text-blue-700">Grade Levels</div>
                                </div>
                                <div className="text-center p-4 bg-purple-50 rounded-lg">
                                    <Users className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                                    <div className="text-2xl font-bold text-purple-900">
                                        {subject.assignments.filter((a) => a.streamId).length}
                                    </div>
                                    <div className="text-sm text-purple-700">Stream Assignments</div>
                                </div>
                                <div className="text-center p-4 bg-red-50 rounded-lg">
                                    <div className="w-8 h-8 mx-auto mb-2 flex items-center justify-center">
                                        <span className="text-red-600 font-bold text-2xl">*</span>
                                    </div>
                                    <div className="text-2xl font-bold text-red-900">
                                        {subject.assignments.filter((a) => a.isRequired).length}
                                    </div>
                                    <div className="text-sm text-red-700">Required Assignments</div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* History */}
                    <Card>
                        <CardHeader>
                            <CardTitle className="flex items-center gap-2">
                                <Calendar className="h-5 w-5" />
                                History
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                <div>
                                    <label className="font-medium text-gray-600">Created:</label>
                                    <p>{new Date(subject.createdAt).toLocaleString()}</p>
                                </div>
                                <div>
                                    <label className="font-medium text-gray-600">Last Updated:</label>
                                    <p>{new Date(subject.updatedAt).toLocaleString()}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </DialogContent>
        </Dialog>
    )
}
