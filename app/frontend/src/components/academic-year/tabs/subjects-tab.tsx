import { useCallback, useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Plus, BookOpen, Search, Edit, Trash } from "lucide-react"
import { SubjectSetupCard } from "@/components/academic-year/form-setup"
import { YearSetupType } from "@/lib/api-response-type"
import { useFieldArray, useFormContext } from "react-hook-form"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { useQueries } from "@tanstack/react-query"
import { toast } from "sonner"
import { sharedApi } from "@/api"
import { GradeSchema, StreamSchema } from "@/lib/api-response-validation"
import z from "zod"


const GRADE_FIELDS = GradeSchema.keyof().options;
const STREAM_FIELDS = StreamSchema.keyof().options;

export default function SubjectsTab({
    onDirty,
}: {
    onDirty: (dirty: boolean) => void
}) {
    const { formState, control, watch, setValue, getValues } = useFormContext<YearSetupType>()

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
        control: control,
        name: "subjects",
        keyName: "rhfId", // Prevents overriding `id`
    })
    const watchForm = watch()

    const fetchSubject = useCallback(async (subjectId: string) => {
        try {

            const selectedSchema = z.object({
                grades: z.array(GradeSchema),
                streams: z.array(StreamSchema),
            });

            const response = await sharedApi.getSubjectDetail(subjectId, selectedSchema, {
                expand: ["grades", "streams"],
                nestedFields: { "grades": GRADE_FIELDS, "streams": STREAM_FIELDS },
            });

            if (!response.success) {
                toast.error(response.error.message, {
                    style: { color: "red" },
                });
                throw new Error(response.error.message);
            }
            return response.data;
        } catch (error) {
            toast.error("Failed to fetch grade details", {
                description: error instanceof Error ? error.message : "Unknown error occurred",
            });
            throw error;
        }
    }, []);

    const subjectQueries = useQueries({
        queries: subjectFields.map((subject) => ({
            queryKey: ['new-subject-detail', subject.id],
            queryFn: () => fetchSubject(subject.id),
            enabled: !!subject.id,
            staleTime: 5 * 60 * 1000, // 5 minutes cache
        })),
    })

    // Update form values when data is fetched
    useEffect(() => {
        if (subjectQueries.some(q => q.isFetching)) return;

        subjectQueries.forEach((query, index) => {
            if (query.isSuccess && query.data && index < subjectFields.length) {
                const { grades, streams } = query.data;

                setValue(`subjects.${index}.grades`, grades);
                setValue(`subjects.${index}.streams`, streams);
            }
        });
    }, [subjectQueries.every(q => q.isFetched)]);

    // Loading state
    const isLoading = subjectQueries.some(query => query.isLoading);

    const filteredSubjects = watchForm.subjects.filter((subject) => {
        const matchesSearch =
            subject.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            subject.code.toLowerCase().includes(searchTerm.toLowerCase())
        return matchesSearch
    })

    const handleCreateSubject = () => {
        prependSubject({ id: "", name: "", code: "", grades: [], streams: [] }); // Add empty subject
        setFormMode("create");
        setFormIndex(0); // Always edit the first subject in the list
        setFormDialogOpen(true);
    };

    return (
        <div className="space-y-6">
            <Card>
                <CardHeader className="pb-4">
                    <CardTitle className="text-xl font-semibold">Subject Management</CardTitle>
                    <p className="text-sm text-gray-500">Configure subjects for your academic year</p>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Search & Add */}
                    <div className="flex flex-col sm:flex-row gap-4">
                        <div className="flex-1">
                            <div className="relative">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
                                <Input
                                    placeholder="Search subjects..."
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                    className="pl-10"
                                />
                            </div>
                        </div>
                        <Button
                            onClick={() => handleCreateSubject()}
                            className="bg-blue-600 hover:bg-blue-700 text-white"
                        >
                            <Plus className="h-4 w-4 mr-2" />
                            Add Subject
                        </Button>
                    </div>

                    {/* Empty State */}
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

                    {/* Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {filteredSubjects.map((subject, index) => (
                            <Card
                                key={subject.id}
                                className="flex flex-col justify-between min-h-[220px] p-4 border border-gray-200 hover:shadow-lg transition-shadow"
                            >
                                {/* Title */}
                                <div>
                                    <CardTitle className="flex items-center gap-2 mb-2 text-md">
                                        <BookOpen className="text-blue-600 shrink-0" />
                                        <span className="truncate">{subject.name}</span>
                                        <Badge className="text-[13px] px-2" variant="outline">
                                            {subject.code}
                                        </Badge>
                                    </CardTitle>

                                    {/* Grades */}
                                    <div className="mt-3">
                                        <h4 className="font-medium mb-3 text-sm text-gray-600">Taught In</h4>
                                        {subject.grades.length > 0 || subject.streams.length > 0 ? (
                                            <div className="flex flex-wrap gap-2">
                                                {subject.grades.map((grade) => (
                                                    <Badge key={grade.id} variant="secondary" className="text-xs">
                                                        Grade {grade.grade}
                                                    </Badge>
                                                ))}
                                                {subject.streams.map((stream) => (
                                                    <Badge key={stream.id} variant="default" className="text-xs">
                                                        {stream.name}
                                                    </Badge>
                                                ))}
                                            </div>
                                        ) : (
                                            <p className="text-xs text-gray-400 italic">No grades assigned</p>
                                        )}
                                    </div>
                                </div>

                                <Separator />

                                {/* Actions */}
                                <div className="flex gap-2 mt-6">
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => removeSubject(index)}
                                        className="flex-1 border-gray-300 hover:bg-red-50"
                                    >
                                        <Trash className="h-4 w-4 mr-1" />
                                        Remove
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={() => {
                                            setFormDialogOpen(true);
                                            setFormMode("edit");
                                            setFormIndex(index);
                                        }}
                                        className="flex-1 border-gray-300 hover:bg-blue-50"
                                    >
                                        <Edit className="h-4 w-4 mr-1" />
                                        Edit
                                    </Button>
                                </div>
                            </Card>
                        ))}
                    </div>
                </CardContent>
            </Card>

            <SubjectSetupCard
                open={formDialogOpen}
                onOpenChange={setFormDialogOpen}
                formIndex={formIndex}
                mode={formMode}
                onDirty={onDirty}
            />
        </div>
    )
}
