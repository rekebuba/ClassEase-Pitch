import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen } from "lucide-react"
import { YearSetupType } from "@/lib/api-response-type"
import { InputWithLabel } from "@/components/inputs/input-labeled"
import { FormProvider, useFieldArray, useForm, useFormContext } from "react-hook-form"
import { useCallback, useEffect, useState } from "react"
import { toast } from "sonner"
import { CheckboxForObject } from "@/components/inputs/checkbox-for-object"
import { debounce } from "lodash"
import { zodResolver } from "@hookform/resolvers/zod"
import { YearSetupSchema } from "@/lib/api-response-validation"

interface SubjectSetupCardProps {
    open: boolean
    onOpenChange: (open: boolean) => void
    formIndex: number
    mode: "create" | "edit"
    onDirty: (dirty: boolean) => void
}
type Grade = YearSetupType["subjects"][number]["grades"] extends Array<infer G> ? G : never
type Subject = YearSetupType["subjects"][number]

export default function SubjectSetupCard({ open, onOpenChange, mode, formIndex, onDirty }: SubjectSetupCardProps) {
    const { control, watch: parentWatch, setValue, getValues } = useFormContext<YearSetupType>()

    const { remove: removeSubject } = useFieldArray({ control: control, name: "subjects" })

    // Isolated sub-form for modal
    const subForm = useForm<Subject>({
        resolver: zodResolver(YearSetupSchema.shape.subjects.element), // validate single subject
        defaultValues: getValues(`subjects.${formIndex}`),
    })
    const { formState: { isDirty }, handleSubmit, watch: subWatch, reset } = subForm

    const watchParentForm = parentWatch()

    // Sync between parent and sub-form
    useEffect(() => {
        if (open) {
            const parentData = getValues(`subjects.${formIndex}`);
            reset(parentData);
        }
    }, [open, formIndex, getValues, reset]);

    // Grade-subject sync logic
    const syncGradesFromSubjects = useCallback(() => {
        const subject = subWatch() || { grades: [] };
        const grades = watchParentForm.grades || [];

        const updatedGrades = grades.map(grade => ({
            ...grade,
            subjects: subject.grades?.some(g => g.id === grade.id)
                ? [...(grade.subjects || []), subject].filter((s, i, arr) =>
                    arr.findIndex(item => item.id === s.id) === i
                )
                : (grade.subjects || []).filter(s => s.id !== subject.id)
        }));

        setValue("grades", updatedGrades, { shouldValidate: false });
    }, [formIndex, watchParentForm?.grades, setValue]);

    // Form submission
    const handleSave = handleSubmit((data) => {
        setValue(`subjects.${formIndex}`, data);
        syncGradesFromSubjects();
        onDirty(isDirty); // Report dirty state
        onOpenChange(false);
        toast.success(mode === "create" ? "New Subject Added" : "Subject updated");
    });

    const handleCancel = () => {
        if (mode === "create") {
            removeSubject(formIndex);
        } else {
            reset(getValues(`subjects.${formIndex}`));
        }
        onOpenChange(false);
    };

    return (
        <Dialog open={open} onOpenChange={handleCancel} >
            <DialogContent className="max-w-3xl">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        {mode === "create" ? "Create New Subject" : "Edit Subject"}
                    </DialogTitle>
                </DialogHeader>

                <div className="space-y-6">
                    {/* Basic Information */}
                    <FormProvider {...subForm}>
                        <Card>
                            <CardHeader>
                                <CardTitle className="text-lg">Basic Information</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <InputWithLabel
                                            fieldTitle="Subject Name *"
                                            nameInSchema={`name`}
                                            placeholder="e.g., Mathematics"
                                        />
                                    </div>

                                    <div>
                                        <InputWithLabel
                                            fieldTitle="Subject Code *"
                                            nameInSchema={`code`}
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
                                        {watchParentForm.grades.map((grade, subjectIndex) => (
                                            <div key={grade.id} className="flex items-center space-x-2">
                                                <CheckboxForObject<Grade>
                                                    fieldTitle={`Grade ${grade.grade}`}
                                                    nameInSchema={`grades`}
                                                    value={subWatch("grades")?.find((g) => g.grade === grade.grade) || {
                                                        id: grade.id,
                                                        yearId: grade.yearId,
                                                        grade: grade.grade,
                                                        level: grade.level,
                                                        hasStream: grade.hasStream,
                                                    }}
                                                    className="w-4 h-4" />
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>

                        {/* Action Buttons */}
                        <div className="flex justify-end gap-3">
                            <Button variant="outline" onClick={handleCancel}>
                                Cancel
                            </Button>
                            <Button
                                disabled={!isDirty}
                                type="submit"
                                onClick={handleSave}
                                className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed"
                            >
                                {mode === "create" ? "Create Subject" : "Update Subject"}
                            </Button>
                        </div>
                    </FormProvider>


                </div>
            </DialogContent>
        </Dialog >
    )
}
