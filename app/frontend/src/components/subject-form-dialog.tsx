import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen } from "lucide-react"
import { YearSetupType } from "@/lib/api-response-type"
import { InputWithLabel } from "./inputs/input-labeled"
import { useFieldArray, UseFormReturn } from "react-hook-form"
import { useState } from "react"
import { toast } from "sonner"

interface SubjectFormDialogProps {
    form: UseFormReturn<YearSetupType>
    open: boolean
    onOpenChange: (open: boolean) => void
    formIndex: number
    mode: "create" | "edit"
}

export function SubjectFormDialog({ form, open, onOpenChange, mode, formIndex }: SubjectFormDialogProps) {
    const { fields: subjectFields, remove: removeSubject } = useFieldArray({ control: form.control, name: "subjects" })
    const [defaultData] = useState(subjectFields[formIndex] || { id: "", name: "", code: "" });

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
            form.setValue(`subjects.${formIndex}`, defaultData);
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
