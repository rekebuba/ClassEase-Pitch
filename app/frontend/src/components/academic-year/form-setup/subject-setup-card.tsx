import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { BookOpen, GraduationCap } from "lucide-react"
import { YearSetupType } from "@/lib/api-response-type"
import { InputWithLabel } from "@/components/inputs/input-labeled"
import { FormProvider, useFieldArray, useForm, useFormContext } from "react-hook-form"
import { useCallback, useEffect, useState } from "react"
import { toast } from "sonner"
import { CheckboxWithLabel } from "@/components/inputs/checkbox-labeled"
import { zodResolver } from "@hookform/resolvers/zod"
import { YearSetupSchema } from "@/lib/api-response-validation"

interface SubjectSetupCardProps {
    open: boolean
    onOpenChange: (open: boolean) => void
    formIndex: number
    mode: "create" | "edit"
}
type Grade = YearSetupType["subjects"][number]["grades"] extends Array<infer G> ? G : never
type Subject = YearSetupType["subjects"][number]
type Stream = YearSetupType["subjects"][number]["streams"][number]

export default function SubjectSetupCard({ open, onOpenChange, mode, formIndex }: SubjectSetupCardProps) {
    const { control, watch: parentWatch, setValue, getValues } = useFormContext<YearSetupType>()

    const { remove: removeSubject } = useFieldArray({ control: control, name: "subjects" })

    // Isolated sub-form for modal
    const subForm = useForm<Subject>({
        resolver: zodResolver(YearSetupSchema.shape.subjects.element), // validate single subject
        defaultValues: getValues(`subjects.${formIndex}`),
    })
    const { formState: { isDirty, dirtyFields }, handleSubmit, watch: subWatch, reset } = subForm

    const watchParentForm = parentWatch()
    const watchSubForm = subWatch()

    // Sync between parent and sub-form
    useEffect(() => {
        if (open) {
            const parentData = getValues(`subjects.${formIndex}`);
            reset(parentData);
        }
    }, [open, formIndex, getValues, reset]);

    // Utility: dedupe and sort by id
    // A process of eliminating redundant copies of data.
    const dedupeAndSort = <T extends { id: string }>(arr: T[]) =>
        arr.filter((v, i, a) => a.findIndex(x => x.id === v.id) === i)
            .sort((a, b) => a.id.localeCompare(b.id));

    const syncGradesFromSubjects = useCallback(() => {
        const subject = watchSubForm || {};
        const grades = watchParentForm.grades || [];

        if (!subject.id) return; // No valid subject to sync

        const subjectEntry = { id: subject.id, name: subject.name, code: subject.code };

        const updatedGrades = grades.map((grade) => {
            const hasThisSubjectInGrade = subject.grades?.some(g => g.id === grade.id);
            const updatedSubjects = !grade.hasStream
                ? dedupeAndSort(
                    hasThisSubjectInGrade
                        ? [...(grade.subjects || []), subjectEntry]
                        : (grade.subjects || []).filter(s => s.id !== subject.id)
                )
                : grade.subjects || [];

            const updatedStreams = (grade.streams || []).map(stream => {
                const hasThisSubjectInStream = subject.streams?.some(st => st.id === stream.id);
                const updatedStreamSubjects = dedupeAndSort(
                    hasThisSubjectInStream
                        ? [...(stream.subjects || []), subjectEntry]
                        : (stream.subjects || []).filter(s => s.id !== subject.id)
                );
                return { ...stream, subjects: updatedStreamSubjects };
            });

            return { ...grade, subjects: updatedSubjects, streams: updatedStreams };
        });

        setValue("grades", updatedGrades, { shouldValidate: false, shouldDirty: true });
    }, [watchSubForm, watchParentForm?.grades, setValue]);

    // Form submission
    const handleSave = handleSubmit((data) => {
        setValue(`subjects.${formIndex}`, data, { shouldDirty: true });
        if (dirtyFields.grades || dirtyFields.streams) {
            syncGradesFromSubjects();
            toast.success(mode === "create" ? "New Grade Added" : "Grade updated");
        }
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
            <DialogContent className="max-w-5xl flex flex-col max-h-[90vh]">
                <DialogHeader className="flex items-center justify-between border-b pb-4 text-lg font-semibold">
                    <div className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5" />
                        <DialogTitle className="flex items-center gap-2">
                            {mode === "create" ? "Create New Subject" : "Edit Subject"}
                        </DialogTitle>
                    </div>
                    <DialogDescription>
                        {watchSubForm?.name
                            ? "Configure"
                            : "Create New"} Subject.
                    </DialogDescription>
                </DialogHeader>

                <FormProvider {...subForm}>
                    <div className="flex-grow overflow-y-auto space-y-4">
                        <Card className="w-full transition-all duration-300">
                            <CardContent className="space-y-6 pt-4 border-t">
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
                                    <div className="pb-3">
                                        <Label className="text-lg font-semibold text-gray-900">Taught in Grades</Label>
                                        <p className="text-sm text-gray-600 mt-1">Select grades and their streams for this subject</p>
                                    </div>

                                    <Card className="shadow-sm">
                                        <CardContent className="p-6">

                                            {/* Empty State */}
                                            {watchParentForm.grades.length === 0 && (
                                                <div className="text-center py-12 text-gray-500">
                                                    <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
                                                    <p>No grades added yet. Add your first grade in the 'Grades & Streams' Tab</p>
                                                </div>
                                            )}

                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                                {watchParentForm.grades.map((grade) => (
                                                    <div
                                                        key={grade.id}
                                                        className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
                                                    >
                                                        {!grade.hasStream ? (
                                                            <div className="flex flex-col space-x-4 space-y-4">
                                                                <CheckboxWithLabel<Subject, Grade>
                                                                    fieldTitle={`Grade ${grade.grade}`}
                                                                    nameInSchema="grades"
                                                                    value={watchSubForm.grades?.find((g) => g.id === grade.id) || { id: grade.id }}
                                                                    className="h-5 w-5 text-primary"
                                                                />
                                                                <Label className="text-sm font-medium">
                                                                    <p className="text-xs text-gray-400 italic">No Stream assigned</p>
                                                                </Label>
                                                            </div>
                                                        ) : (
                                                            <div className="space-y-3">
                                                                <div className="flex items-center space-x-3">
                                                                    <label>{`Grade ${grade.grade}`}</label>
                                                                </div>

                                                                <div className="ml-8 space-y-2">
                                                                    {grade.streams.map((stream) => (
                                                                        <div key={stream.id} className="flex items-center space-x-3">
                                                                            <CheckboxWithLabel<Subject, Stream>
                                                                                fieldTitle={`Grade ${grade.grade} (${stream.name})`}
                                                                                nameInSchema="streams"
                                                                                value={
                                                                                    watchSubForm.streams?.find((s) => s.id === stream.id) || {
                                                                                        id: stream.id,
                                                                                        gradeId: stream.gradeId,
                                                                                    }
                                                                                }
                                                                                className="h-4 w-4 text-primary"
                                                                            />
                                                                        </div>
                                                                    ))}
                                                                </div>
                                                            </div>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                        </CardContent>
                                    </Card>
                                </div>
                            </CardContent>
                        </Card>
                    </div>

                    {/* Action Buttons */}
                    <DialogFooter className="sticky bottom-0 bg-white border-t p-4 z-10">
                        <div className="ml-auto flex gap-3">
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
                    </DialogFooter>
                </FormProvider>
            </DialogContent>
        </Dialog >
    )
}
