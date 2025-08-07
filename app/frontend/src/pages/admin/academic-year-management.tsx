import { useEffect, useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Plus, Search, Filter, Calendar, Edit } from "lucide-react"
// import type { AcademicYear } from "@/lib/academic-year"
import { AcademicYearViewCard, AcademicYearDetailView } from "@/components"
import { AcademicYearSetup } from "@/pages/admin"
import { GradeSchema, YearSchema } from "@/lib/api-response-validation"
import { sharedApi } from "@/api"
import { Year } from "@/lib/api-response-type"
import { pickFields } from "@/utils/pick-zod-fields"
import { toast } from "sonner"
import { z } from "zod"
import { DetailAcademicYear } from "@/components/academic-year-view-card"
import { useQuery } from "@tanstack/react-query"

export type AcademicYear = Pick<Year, "id" | "calendarType" | "name" | "startDate" | "endDate" | "status" | "createdAt" | "updatedAt">;

export default function AcademicYearManagement() {
    // const [academicYears, setAcademicYears] = useState<AcademicYear[]>([])
    const [searchTerm, setSearchTerm] = useState("")
    const [statusFilter, setStatusFilter] = useState<string>("all")
    const [currentView, setCurrentView] = useState<"list" | "detail" | "edit" | "create">("list")
    const [selectedAcademicYear, setSelectedAcademicYear] = useState<DetailAcademicYear | null>(null)

    const fetchAcademicYear = async () => {
        const fields = [
            "id",
            "calendarType",
            "name",
            "startDate",
            "endDate",
            "status",
            "createdAt",
            "updatedAt",
        ] as const
        const selectYearSchema = pickFields(YearSchema, fields);

        const response = await sharedApi.getYear(z.array(selectYearSchema), {
            fields: [...fields],
        });

        if (!response.success) {
            toast.error(response.error.message, {
                style: { color: "red" },
            });
            throw new Error(response.error.message);
        }

        return response.data;
    };

    const { data: academicYears, error, isLoading } = useQuery({
        queryKey: ["academicYears"],
        queryFn: fetchAcademicYear,
    })

    if (error) return <div>Error loading academic years: {error.message}</div>
    if (isLoading) return <div>Loading academic years...</div>
    if (!academicYears) return <div>No academic years found.</div>

    const filteredAcademicYears = academicYears.filter((year) => {
        const matchesSearch = year.name.toLowerCase().includes(searchTerm.toLowerCase())
        const matchesStatus = statusFilter === "all" || year.status === statusFilter
        return matchesSearch && matchesStatus
    })

    const handleView = (detailAcademicYear: DetailAcademicYear) => {
        setSelectedAcademicYear(detailAcademicYear)
        setCurrentView("detail")
    }

    const handleEdit = (detailAcademicYear: DetailAcademicYear) => {
        setSelectedAcademicYear(detailAcademicYear)
        setCurrentView("edit")
    }

    const handleCreate = () => {
        setSelectedAcademicYear(null)
        setCurrentView("create")
    }

    const handleBack = () => {
        setCurrentView("list")
        setSelectedAcademicYear(null)
    }

    const handleActivate = (academicYear: AcademicYear) => {
        // First deactivate any currently active year
        const updatedYears = academicYears.map((year) => ({
            ...year,
            status: year.status === "active" ? ("completed" as const) : year.status,
        }))

        // Then activate the selected year
        const finalYears = updatedYears.map((year) =>
            year.id === academicYear.id ? { ...year, status: "active" as const, updatedAt: new Date().toISOString() } : year,
        )

        // setAcademicYears(finalYears)
    }

    const handleArchive = (academicYear: AcademicYear) => {
        const updatedYears = academicYears.map((year) =>
            year.id === academicYear.id
                ? { ...year, status: "completed" as const, updatedAt: new Date().toISOString() }
                : year,
        )
        // setAcademicYears(updatedYears)
    }

    const handleDuplicate = (academicYear: AcademicYear) => {
        const newYear: AcademicYear = {
            ...academicYear,
            id: Date.now().toString(),
            name: `${academicYear.name} (Copy)`,
            status: "draft",
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
        }
        // setAcademicYears([newYear, ...academicYears])
    }

    const handleSave = (academicYear: AcademicYear) => {
        if (selectedAcademicYear) {
            // Update existing
            const updatedYears = academicYears.map((year) =>
                year.id === selectedAcademicYear.id ? { ...academicYear, updatedAt: new Date().toISOString() } : year,
            )
            // setAcademicYears(updatedYears)
        } else {
            // Create new
            const newYear: AcademicYear = {
                ...academicYear,
                id: Date.now().toString(),
                createdAt: new Date().toISOString(),
                updatedAt: new Date().toISOString(),
            }
            // setAcademicYears([newYear, ...academicYears])
        }
        setCurrentView("list")
        setSelectedAcademicYear(null)
    }

    const getStatusCounts = () => {
        return {
            total: academicYears.length,
            active: academicYears.filter((y) => y.status === "active").length,
            draft: academicYears.filter((y) => y.status === "draft").length,
            completed: academicYears.filter((y) => y.status === "completed").length,
        }
    }

    const statusCounts = getStatusCounts()

    // Render different views
    if (currentView === "detail" && selectedAcademicYear) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
                <div className="max-w-7xl mx-auto">
                    <AcademicYearDetailView
                        detailAcademicYears={selectedAcademicYear}
                        onBack={handleBack}
                        onEdit={() => handleEdit(selectedAcademicYear)}
                    />
                </div>
            </div>
        )
    }

    if (currentView === "edit" && selectedAcademicYear) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
                <div className="max-w-7xl mx-auto">
                    <AcademicYearSetup initialData={selectedAcademicYear} onSave={handleSave} onCancel={handleBack} mode="edit" />
                </div>
            </div>
        )
    }

    if (currentView === "create") {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
                <div className="max-w-7xl mx-auto">
                    <AcademicYearSetup onSave={handleSave} onCancel={handleBack} mode="create" />
                </div>
            </div>
        )
    }

    // Main list view
    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
            <div className="max-w-7xl mx-auto space-y-6">
                {/* Header */}
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900">Academic Year Management</h1>
                        <p className="text-gray-600 mt-1">Manage and configure your school's academic years</p>
                    </div>
                    <Button onClick={handleCreate}>
                        <Plus className="h-4 w-4 mr-2" />
                        Create New Academic Year
                    </Button>
                </div>

                {/* Stats Overview */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <Card>
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Total Years</p>
                                    <p className="text-2xl font-bold">{statusCounts.total}</p>
                                </div>
                                <Calendar className="h-8 w-8 text-blue-600" />
                            </div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Active</p>
                                    <p className="text-2xl font-bold text-green-600">{statusCounts.active}</p>
                                </div>
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                    <div className="w-3 h-3 bg-green-600 rounded-full" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Draft</p>
                                    <p className="text-2xl font-bold text-yellow-600">{statusCounts.draft}</p>
                                </div>
                                <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                                    <Edit className="h-4 w-4 text-yellow-600" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Completed</p>
                                    <p className="text-2xl font-bold text-gray-600">{statusCounts.completed}</p>
                                </div>
                                <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                                    <div className="w-3 h-3 bg-gray-600 rounded-full" />
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Filters and Search */}
                <Card>
                    <CardContent className="p-4">
                        <div className="flex flex-col md:flex-row gap-4">
                            <div className="flex-1">
                                <div className="relative">
                                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                                    <Input
                                        placeholder="Search academic years..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                        className="pl-10"
                                    />
                                </div>
                            </div>
                            <div className="flex items-center gap-2">
                                <Filter className="h-4 w-4 text-gray-500" />
                                <Select value={statusFilter} onValueChange={setStatusFilter}>
                                    <SelectTrigger className="w-48">
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="all">All Status</SelectItem>
                                        <SelectItem value="active">Active</SelectItem>
                                        <SelectItem value="draft">Draft</SelectItem>
                                        <SelectItem value="completed">Completed</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                {/* Academic Years List */}
                <div className="space-y-4">
                    {filteredAcademicYears.length > 0 ? (
                        filteredAcademicYears.map((academicYear) => (
                            <AcademicYearViewCard
                                key={academicYear.id}
                                academicYear={academicYear}
                                onView={handleView}
                                onEdit={handleEdit}
                                onActivate={handleActivate}
                                onArchive={handleArchive}
                                onDuplicate={handleDuplicate}
                            />
                        ))
                    ) : (
                        <Card>
                            <CardContent className="p-12 text-center">
                                <Calendar className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                                <h3 className="text-lg font-medium text-gray-900 mb-2">No Academic Years Found</h3>
                                <p className="text-gray-600 mb-4">
                                    {searchTerm || statusFilter !== "all"
                                        ? "No academic years match your current filters."
                                        : "Get started by creating your first academic year."}
                                </p>
                                {!searchTerm && statusFilter === "all" && (
                                    <Button onClick={handleCreate}>
                                        <Plus className="h-4 w-4 mr-2" />
                                        Create Academic Year
                                    </Button>
                                )}
                            </CardContent>
                        </Card>
                    )}
                </div>
            </div>
        </div>
    )
}
