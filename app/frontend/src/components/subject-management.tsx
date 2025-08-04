import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, BookOpen, Search, Edit, Trash } from "lucide-react"
import { SubjectFormDialog } from "./subject-form-dialog"
import { YearSetupType } from "@/lib/api-response-type"
import { useFieldArray, UseFormReturn } from "react-hook-form"
import { Badge } from "./ui/badge"
import { Separator } from "./ui/separator"

interface SubjectManagementProps {
    form: UseFormReturn<YearSetupType>
}

export default function SubjectManagement({ form }: SubjectManagementProps) {
    const [searchTerm, setSearchTerm] = useState("")
    const [formDialogOpen, setFormDialogOpen] = useState(false)
    const [formMode, setFormMode] = useState<"create" | "edit">("create")
    const [formIndex, setFormIndex] = useState<number>(0)

    const {
        fields: subjectFields,
        append: appendSubject,
        prepend: prependSubject,
        remove: removeSubject,
    } = useFieldArray({
        control: form.control,
        name: "subjects",
    })
    const watchForm = form.watch()

    const filteredSubjects = watchForm.subjects.filter((subject) => {
        const matchesSearch =
            subject.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            subject.code.toLowerCase().includes(searchTerm.toLowerCase())
        return matchesSearch
    })

    const handleCreateSubject = () => {
        prependSubject({ id: "", name: "", code: "" }); // Add empty subject
        setFormMode("create");
        setFormIndex(0); // Always edit the first subject in the list
        setFormDialogOpen(true);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader>
                    <CardTitle>Subject Management</CardTitle>
                    <p className="text-sm text-gray-600">Configure subjects for your academic year</p>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Search Controls */}
                    <div className="flex flex-col sm:flex-row gap-4">
                        <div className="flex-1">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                                <Input
                                    placeholder="Search subjects..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="pl-10"
                                />
                            </div>
                        </div>
                        <Button onClick={() => handleCreateSubject()}>
                            <Plus className="h-4 w-4 mr-2" />
                            Add Subject
                        </Button>
                    </div>

                    {filteredSubjects.length === 0 && (
                        <div className="text-center py-12 text-gray-500">
                            <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
                            <p>
                                {subjectFields.length === 0
                                    ? "No subjects added yet. Add your first subject above."
                                    : "No subjects match your search criteria."}
                            </p>
                        </div>
                    )}

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {filteredSubjects.map((subject, index) => (
                            <Card key={subject.id} className="p-4 hover:shadow-md transition-shadow">
                                <CardTitle className="flex items-center gap-2 mb-2 text-md">
                                    <BookOpen className="text-blue-600" />
                                    {subject.name}
                                    <Badge className="text-[13px] px-2" variant={"outline"}>
                                        {subject.code}
                                    </Badge>
                                </CardTitle>
                                <CardContent className="p-4">
                                    <Separator />
                                    <div className="flex gap-2 mt-4 flex-wrap">
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => removeSubject(index)}
                                            className="flex-1 bg-transparent"
                                        >
                                            <Trash className="h-4 w-4 mr-2" />
                                            Remove
                                        </Button>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            className="flex-1 bg-transparent"
                                            onClick={() => {
                                                setFormDialogOpen(true)
                                                setFormMode("edit")
                                                setFormIndex(index)
                                            }}
                                        >
                                            <Edit className="h-4 w-4 mr-2" />
                                            Edit
                                        </Button>
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </CardContent>

                <SubjectFormDialog
                    form={form}
                    open={formDialogOpen}
                    onOpenChange={setFormDialogOpen}
                    formIndex={formIndex}
                    mode={formMode}
                />
            </Card>
        </div >
    )
}
