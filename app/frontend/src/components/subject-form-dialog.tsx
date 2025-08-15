import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen } from "lucide-react"
import { YearSetupType } from "@/lib/api-response-type"
import { InputWithLabel } from "./inputs/input-labeled"
import { useFieldArray, UseFormReturn } from "react-hook-form"
import { useEffect, useState } from "react"
import { toast } from "sonner"
import { CheckboxWithLabel } from "./inputs/checkbox-labeled"

interface SubjectFormDialogProps {
    form: UseFormReturn<YearSetupType>
    open: boolean
    onOpenChange: (open: boolean) => void
    formIndex: number
    mode: "create" | "edit"
}
type Grade = YearSetupType["subjects"][number]["grades"] extends Array<infer G> ? G : never


export function SubjectFormDialog({ form, open, onOpenChange, mode, formIndex }: SubjectFormDialogProps) {
    const { fields: subjectFields, remove: removeSubject } = useFieldArray({ control: form.control, name: "subjects" })
    const [defaultData, setDefaultData] = useState();

    const watchForm = form.watch()

    useEffect(() => {
        if (open && mode === "edit") {
            const subjectData = form.getValues().subjects[formIndex];
            if (subjectData) {
                setDefaultData(JSON.parse(JSON.stringify(subjectData)));
            }
        }
    }, [open, formIndex, form, mode]);

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
            removeSubject(formIndex);
        } else {
            if (defaultData) {
                form.setValue(`subjects.${formIndex}`, defaultData);
            }
        }
        onOpenChange(false);
    };


    return (
        <Dialog open={open} onOpenChange={handleCancel}>
            <DialogContent className="max-w-3xl">
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
                                    <InputWithLabel
                                        fieldTitle="Subject Name *"
                                        nameInSchema={`subjects.${formIndex}.name`}
                                        placeholder="e.g., Mathematics"
                                    />
                                </div>

                                <div>
                                    <InputWithLabel
                                        fieldTitle="Subject Code *"
                                        nameInSchema={`subjects.${formIndex}.code`}
                                        placeholder="e.g., MATH"
                                    />
                                </div>
                            </div>

                            <div>
                                <Label htmlFor="description">Description (Optional)</Label>
                                <Textarea
                                    id="description"
                                    placeholder="Brief description of the subject..."
                                    rows={3}
                                />
                            </div>

                            <div>
                                <Label>Taught in Grades:</Label>
                                <p className="text-sm text-gray-500 mb-3">Selected Grade for this Subject</p>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    {watchForm.grades.map((grade, subjectIndex) => (
                                        <div key={grade.id} className="flex items-center space-x-2">
                                            <CheckboxWithLabel<Grade>
                                                fieldTitle={`Grade ${grade.grade}`}
                                                nameInSchema={`subjects.${formIndex}.grades`}
                                                value={watchForm.subjects[formIndex].grades.find((g) => g.grade === grade.grade) || grade}
                                                className="w-4 h-4" />
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Action Buttons */}
                    <div className="flex justify-end gap-3">
                        <Button variant="outline" onClick={() => handleCancel()}>
                            Cancel
                        </Button>
                        <Button onClick={() => handleSave()}>
                            {mode === "create" ? "Create Subject" : "Update Subject"}
                        </Button>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    )
}
