import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Save, Eye } from "lucide-react"
import { DetailAcademicYear } from "@/components/academic-year-view-card"
import { zodResolver } from "@hookform/resolvers/zod"
import { FormProvider, useForm } from "react-hook-form"
import { YearSetupSchema } from "@/lib/api-response-validation"
import type { YearSetupType } from "@/lib/api-response-type"
import { UnsavedChangesDialog } from "@/components/unsaved-changes-dialog"
import { AcademicYearTabs } from "@/components/academic-year/academic-year-tabs"

interface AcademicYearSetupProps {
    initialData?: DetailAcademicYear
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

    // const [defaultNestedGrade, setDefaultNestedGrade] = useState<YearSetupType["grades"]>([])

    const defaultValues: YearSetupType = {
        year: {
            id: initialData ? initialData.id : crypto.randomUUID(),
            calendarType: initialData ? initialData.calendarType : "" as "Semester",
            name: initialData ? initialData.name : "",
            startDate: initialData ? initialData.startDate : "",
            endDate: initialData ? initialData.endDate : "",
            status: initialData ? initialData.status : "",
            createdAt: initialData ? initialData.createdAt : "",
            updatedAt: initialData ? initialData.updatedAt : ""
        },
        grades: initialData ? initialData.grades.map((grade) => ({
            ...grade,
            yearId: "",
            sections: [],
            subjects: [],
            streams: [],
        }))
            : [],
        subjects: initialData ? initialData.subjects.map((subject) => ({
            ...subject,
            grades: [],
            streams: [],
        })) : [],
    }

    const form = useForm<YearSetupType>({
        resolver: zodResolver(YearSetupSchema),
        defaultValues
    })
    const watchForm = form.watch()

    function requestTabChange(nextTab: string) {
        if (unsavedChanges) {
            setPendingTab(nextTab)
            setDialogOpen(true)
        } else {
            setActiveTab(nextTab)
        }
    }

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
                            onTabChange={requestTabChange}
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
