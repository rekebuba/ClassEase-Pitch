import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen, ChevronDown, ChevronRight } from "lucide-react"
import { Year, YearSetupType } from "@/lib/api-response-type"
import { InputWithLabel } from "@/components/inputs/input-labeled"
import { FormProvider, useFieldArray, useForm, useFormContext } from "react-hook-form"
import { useCallback, useEffect, useState } from "react"
import { toast } from "sonner"
import { CheckboxForObject } from "@/components/inputs/checkbox-for-object"
import { debounce } from "lodash"
import { zodResolver } from "@hookform/resolvers/zod"
import { YearSetupSchema } from "@/lib/api-response-validation"
import { Collapsible, CollapsibleTrigger } from "@/components/ui/collapsible"

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

    // Grade-subject sync logic
    const syncGradesFromSubjects = useCallback(() => {
        const subject = watchSubForm || {};
        const grades = watchParentForm.grades || [];

        const updatedGrades = grades.map((grade) => {
            const hasThisSubject = subject.grades?.some((g) => g.id === grade.id);

            // Extract minimal subject info for insertion
            const subjectEntry = subject.id
                ? { id: subject.id, name: subject.name, code: subject.code }
                : null;

            const updatedSubjects = hasThisSubject
                ? [
                    ...(grade.subjects || []),
                    subjectEntry!,
                ].filter(
                    (s, i, arr) => s && arr.findIndex((item) => item.id === s.id) === i
                )
                : (grade.subjects || []).filter((s) => s.id !== subject.id);

            return { ...grade, subjects: updatedSubjects };
        });

        setValue("grades", updatedGrades, { shouldValidate: false, shouldDirty: true });
    }, [watchSubForm, watchParentForm?.grades, setValue]);

    // Form submission
    const handleSave = handleSubmit((data) => {
        setValue(`subjects.${formIndex}`, data, { shouldDirty: true });
        if (dirtyFields.grades) {
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

    const [expandedGrades, setExpandedGrades] = useState<Set<string>>(new Set())

    const toggleGrade = (gradeId: string) => {
        const newExpanded = new Set(expandedGrades)
        if (newExpanded.has(gradeId)) {
            newExpanded.delete(gradeId)
        } else {
            newExpanded.add(gradeId)
        }
        setExpandedGrades(newExpanded)
    }

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

                                    <Card>
                                        <CardContent className="space-y-4 mt-4">
                                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                                {watchParentForm.grades.map((grade) => (
                                                    <div
                                                        key={grade.id}
                                                        className="rounded-lg overflow-hidden"
                                                    >
                                                        <div className="flex">

                                                            <div className="flex items-center space-x-2 mb-2">
                                                                <CheckboxForObject<Grade>
                                                                    fieldTitle={`Grade ${grade.grade}`}
                                                                    nameInSchema={`grades`}
                                                                    value={
                                                                        watchSubForm.grades?.find((g) => g.grade === grade.grade) || {
                                                                            grade: grade.grade,
                                                                            hasStream: grade.hasStream,
                                                                            id: grade.id,
                                                                            level: grade.level,
                                                                            yearId: grade.yearId,
                                                                        }
                                                                    }
                                                                    className="w-4 h-4"
                                                                />
                                                            </div>
                                                            {grade.hasStream && grade.streams.length > 0 && (
                                                                <div className="pl-4">
                                                                    <span className="text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded">
                                                                        {watchSubForm.streams?.filter((s) => grade.streams.find((gs) => gs.id === s.id)).length}{" "}
                                                                        stream(s) selected
                                                                    </span>
                                                                    <Collapsible open={true} onOpenChange={() => toggleGrade(grade.id)}>
                                                                        <CollapsibleTrigger className="p-1 hover:bg-gray-200 rounded">
                                                                            {true ? (
                                                                                <ChevronDown className="h-4 w-4 text-gray-500" />
                                                                            ) : (
                                                                                <ChevronRight className="h-4 w-4 text-gray-500" />
                                                                            )}
                                                                        </CollapsibleTrigger>
                                                                    </Collapsible>
                                                                </div>
                                                            )}
                                                        </div>
                                                        {grade.hasStream && (
                                                            <div className="ml-3 pl-4 border-l border-gray-600 space-y-2">
                                                                {grade.streams.map((stream) => (
                                                                    <div key={stream.id} className="flex items-center space-x-2">
                                                                        <CheckboxForObject<Stream>
                                                                            fieldTitle={stream.name}
                                                                            nameInSchema={`streams`}
                                                                            value={
                                                                                watchSubForm.streams?.find((s) => s.id === stream.id) || {
                                                                                    id: stream.id,
                                                                                    gradeId: stream.gradeId,
                                                                                    name: stream.name,
                                                                                }
                                                                            }
                                                                            className="w-4 h-4"
                                                                        />
                                                                    </div>
                                                                ))}
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
