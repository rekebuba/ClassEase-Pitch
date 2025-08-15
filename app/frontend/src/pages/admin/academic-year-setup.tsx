import { useCallback, useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Save, Eye } from "lucide-react"
import { DetailAcademicYear } from "@/components/academic-year-view-card"
import { zodResolver } from "@hookform/resolvers/zod"
import { FormProvider, useForm } from "react-hook-form"
import { GradeSchema, SectionSchema, StreamSchema, SubjectSchema, YearSetupSchema } from "@/lib/api-response-validation"
import type { YearSetupType } from "@/lib/api-response-type"
import { UnsavedChangesDialog } from "@/components/unsaved-changes-dialog"
import { AcademicYearTabs } from "@/components/academic-year/academic-year-tabs"
import type { AcademicYear } from "./academic-year-management"
import z from "zod"
import sharedApi from "@/api/sharedApi"
import { toast } from "sonner"
import { debounce } from "lodash"
import { useQuery } from "@tanstack/react-query"

interface AcademicYearSetupProps {
    initialData?: AcademicYear
    onSave?: (academicYear: DetailAcademicYear) => void
    onCancel?: () => void
    mode?: "create" | "edit"
}

export default function AcademicYearSetup({
    initialData,
    onSave,
    onCancel,
    mode = "create",
}: AcademicYearSetupProps) {
    const [activeTab, setActiveTab] = useState("basic")
    const [unsavedChanges, setUnsavedChanges] = useState(false)
    const [pendingTab, setPendingTab] = useState<string | null>(null)
    const [dialogOpen, setDialogOpen] = useState(false)

    const [defaultValues] = useState<YearSetupType>({
        id: crypto.randomUUID(),
        calendarType: "" as "Semester",
        name: "",
        startDate: "",
        endDate: "",
        status: "",
        createdAt: "",
        updatedAt: "",
        grades: [],
        subjects: [],
    })

    // Fetch grade detail
    const fetchGrade = useCallback(async (yearId: string): Promise<YearSetupType['grades']> => {
        try {
            const schema = z.array(
                GradeSchema.extend({
                    subjects: z.array(SubjectSchema),
                    sections: z.array(SectionSchema),
                    streams: z.array(StreamSchema.extend({
                        subjects: z.array(SubjectSchema),
                    })),
                })
            )

            const response = await sharedApi.getGrade(yearId, schema)

            if (!response.success) throw new Error(response.error.message)

            return response.data
        } catch (error) {
            toast.error("Failed to fetch grade details", {
                description: error instanceof Error ? error.message : "Unknown error occurred",
            })
            throw error
        }
    }, [])

    // Fetch subject detail
    const fetchSubject = useCallback(async (yearId: string): Promise<YearSetupType['subjects']> => {
        try {
            const schema = z.array(
                SubjectSchema.extend({
                    grades: z.array(GradeSchema),
                    streams: z.array(StreamSchema),
                }))

            const response = await sharedApi.getSubject(yearId, schema)

            if (!response.success) throw new Error(response.error.message)

            return response.data
        } catch (error) {
            toast.error("Failed to fetch grade details", {
                description: error instanceof Error ? error.message : "Unknown error occurred",
            })
            throw error
        }
    }, [])

    const form = useForm<YearSetupType>({
        resolver: zodResolver(YearSetupSchema),
        defaultValues
    })
    const watchForm = form.watch()

    const gradeQuery = useQuery({
        queryKey: ['grades', initialData?.id],
        queryFn: () => initialData?.id ? fetchGrade(initialData.id) : null,
        enabled: !!initialData?.id,
        staleTime: 0,
        gcTime: 0,
    });

    const subjectQuery = useQuery({
        queryKey: ['subjects', initialData?.id],
        queryFn: () => initialData?.id ? fetchSubject(initialData.id) : null,
        enabled: !!initialData?.id,
        staleTime: 0,
        gcTime: 0,
    });

    // Combined effect
    useEffect(() => {
        if (
            gradeQuery.isSuccess && gradeQuery.data &&
            subjectQuery.isSuccess && subjectQuery.data &&
            initialData
        ) {
            form.reset({
                ...initialData,
                grades: gradeQuery.data,
                subjects: subjectQuery.data,
            });
        }
    }, [gradeQuery.isSuccess, subjectQuery.isSuccess, initialData, form]);

    function discardAndContinue() {
        setUnsavedChanges(false)
        if (pendingTab) {
            setActiveTab(pendingTab)
            setPendingTab(null)
        }
        setDialogOpen(false)
    }

    const submitForm = (values: YearSetupType) => {
        // onSave?.(values)
        setUnsavedChanges(false)
    }

    console.log("watchForm:", watchForm)

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
            <div className="max-w-7xl mx-auto space-y-6">
                {/* Header */}
                <header className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">
                            {mode === "edit" ? "Edit Academic Year" : "Academic Year Setup"}
                        </h1>
                        <p className="text-gray-600 mt-1">
                            {mode === "edit"
                                ? "Modify your academic year configuration"
                                : "Configure your school's academic year structure"}
                        </p>
                    </div>
                    <div className="flex items-center gap-3">
                        {onCancel && (
                            <Button variant="outline" onClick={onCancel}>
                                Cancel
                            </Button>
                        )}
                        <Button variant="outline">
                            <Eye className="h-4 w-4 mr-2" />
                            Preview
                        </Button>
                        <Button
                            disabled={!unsavedChanges}
                            type="submit"
                            form="academic-year-form"
                            className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed"
                        >
                            <Save className="h-4 w-4 mr-2" />
                            {mode === "edit" ? "Update Academic Year" : "Save Academic Year"}
                        </Button>
                    </div>
                </header>

                <FormProvider {...form}>
                    <form
                        onSubmit={form.handleSubmit(submitForm)}
                    // className="flex flex-col md:flex-row gap-4 md:gap-8"
                    >
                        <AcademicYearTabs
                            activeTab={activeTab}
                            onTabChange={setActiveTab}
                            onUnsavedChange={setUnsavedChanges}
                        />

                        {/* Confirmation Dialog */}
                        <UnsavedChangesDialog
                            open={dialogOpen}
                            onStay={() => setDialogOpen(false)}
                            onDiscard={discardAndContinue}
                        />
                    </form>
                </FormProvider>
            </div>
        </div >
    )
}
