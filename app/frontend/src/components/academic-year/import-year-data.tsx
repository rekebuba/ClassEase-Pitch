import sharedApi from "@/api/sharedApi";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Progress } from "@/components/ui/progress";
import { Year } from "@/lib/api-response-type";
import {
  GradeSchema,
  SubjectSchema,
  YearSchema,
} from "@/lib/api-response-validation";
import { useQuery } from "@tanstack/react-query";
import {
  AlertCircle,
  BookOpen,
  CheckCircle,
  Download,
  GraduationCap,
  Loader2,
  Save,
} from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";
import z from "zod";
import { Skeleton } from "../ui/skeleton";

interface AcademicYearActionBarProps {
  mode: "create" | "edit";
  onCancel?: () => void;
  unsavedChanges: boolean;
}

export function AcademicYearActionBar({
  mode,
  unsavedChanges,
  onCancel,
}: AcademicYearActionBarProps) {
  return (
    <div className="flex items-center gap-3">
      <Button variant="outline" onClick={onCancel}>
        Cancel
      </Button>
      <ImportDataDialog />
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
  );
}

interface PreviousAcademicYear extends Year {
  gradesCount: number;
  subjectsCount: number;
}

interface ImportOptions {
  importGrades: boolean;
  importSubjects: boolean;
}

interface ImportDataDialogProps {
  onImport?: (
    selectedYear: PreviousAcademicYear,
    importOptions: ImportOptions,
  ) => void;
}

export function ImportDataDialog({ onImport }: ImportDataDialogProps) {
  const fetchAcademicYear = async (): Promise<PreviousAcademicYear[]> => {
    const Schema = YearSchema.extend({
      grades: z.array(GradeSchema.pick({ id: true })),
      subjects: z.array(SubjectSchema.pick({ id: true })),
    });

    const response = await sharedApi.getYear(z.array(Schema));

    if (!response.success) {
      toast.error(response.error.message, {
        style: { color: "red" },
      });
      throw new Error(response.error.message);
    }

    const result = response.data.map((year) => ({
      ...year,
      gradesCount: year.grades.length,
      subjectsCount: year.subjects.length,
    }));

    return result;
  };

  const { data: years, isLoading } = useQuery({
    queryKey: ["years"],
    queryFn: fetchAcademicYear,
  });

  const [isOpen, setIsOpen] = useState(false);
  const [selectedYear, setSelectedYear] = useState<PreviousAcademicYear | null>(
    null,
  );
  const [importOptions, setImportOptions] = useState<ImportOptions>({
    importGrades: true,
    importSubjects: true,
  });
  const [isImporting, setIsImporting] = useState(false);
  const [importProgress, setImportProgress] = useState(0);
  const [importStep, setImportStep] = useState("");

  const handleImport = async () => {
    if (!selectedYear) return;

    setIsImporting(true);
    setImportProgress(0);

    // Simulate import process
    const steps = [
      "Connecting to database...",
      "Retrieving grade structure...",
      "Loading subjects data...",
      "Processing stream configurations...",
      "Validating data integrity...",
      "Finalizing import...",
    ];

    for (let i = 0; i < steps.length; i++) {
      setImportStep(steps[i]);
      setImportProgress((i + 1) * (100 / steps.length));
      await new Promise((resolve) => setTimeout(resolve, 800));
    }

    // Complete import
    setTimeout(() => {
      setIsImporting(false);
      setImportProgress(100);
      setImportStep("Import completed successfully!");

      if (onImport) {
        onImport(selectedYear, importOptions);
      }

      setTimeout(() => {
        setIsOpen(false);
        setSelectedYear(null);
        setImportProgress(0);
        setImportStep("");
      }, 1500);
    }, 500);
  };

  const getStatusColor = (status: Year["status"]) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800 border-green-200";
      case "active":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "draft":
        return "bg-gray-100 text-gray-800 border-gray-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  if (isLoading) {
    return (
      <div>
        <h3 className="font-medium mb-4">Select Academic Year</h3>
        <div className="grid gap-3">
          {[...Array(3)].map((_, i) => (
            <Card key={i} className="cursor-pointer">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    {/* Circle placeholder */}
                    <Skeleton className="w-4 h-4 rounded-full" />
                    <div>
                      <Skeleton className="h-4 w-32 mb-2" />
                      <Skeleton className="h-3 w-48" />
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    {/* Badge placeholder */}
                    <Skeleton className="h-6 w-16 rounded-full" />
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <Skeleton className="h-4 w-20" />
                      <Skeleton className="h-4 w-20" />
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button variant="outline">
          <Download className="h-4 w-4 mr-2" />
          Import from Previous Year
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-5xl flex flex-col max-h-[90vh]">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Download className="h-5 w-5" />
            Import Academic Year Data
          </DialogTitle>
          <p className="text-sm text-gray-600">
            Select a previous academic year to import grades, subjects, and
            stream configurations
          </p>
        </DialogHeader>

        {!isImporting ? (
          <div className="space-y-6">
            {/* Previous Years Selection */}
            <div>
              <h3 className="font-medium mb-4">Select Academic Year</h3>
              <div className="grid gap-3">
                {years?.map((year) => (
                  <Card
                    key={year.id}
                    className={`cursor-pointer transition-all hover:shadow-md ${
                      selectedYear?.id === year.id
                        ? "ring-2 ring-blue-500 bg-blue-50"
                        : "hover:bg-gray-50"
                    }`}
                    onClick={() => setSelectedYear(year)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-4 h-4 rounded-full border-2 ${
                              selectedYear?.id === year.id
                                ? "bg-blue-500 border-blue-500"
                                : "border-gray-300"
                            }`}
                          >
                            {selectedYear?.id === year.id && (
                              <CheckCircle className="w-4 h-4 text-white" />
                            )}
                          </div>
                          <div>
                            <h4 className="font-medium">{year.name}</h4>
                            <p className="text-sm text-gray-600">
                              {year.startDate} to {year.endDate}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <Badge className={getStatusColor(year.status)}>
                            {year.status}
                          </Badge>
                          <div className="flex items-center gap-4 text-sm text-gray-600">
                            <div className="flex items-center gap-1">
                              <GraduationCap className="h-4 w-4" />
                              {year.gradesCount} grades
                            </div>
                            <div className="flex items-center gap-1">
                              <BookOpen className="h-4 w-4" />
                              {year.subjectsCount} subjects
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Import Options */}
            {selectedYear && (
              <div>
                <h3 className="font-medium mb-4">Import Options</h3>
                <Card>
                  <CardContent className="p-4 space-y-4">
                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="import-grades"
                        checked={importOptions.importGrades}
                        onCheckedChange={(checked) =>
                          setImportOptions((prev) => ({
                            ...prev,
                            importGrades: checked as boolean,
                          }))
                        }
                      />
                      <label
                        htmlFor="import-grades"
                        className="flex items-center gap-2 cursor-pointer"
                      >
                        <GraduationCap className="h-4 w-4" />
                        <div>
                          <div className="font-medium">
                            Import Grades Structure
                          </div>
                          <div className="text-sm text-gray-600">
                            Import all grade levels and their configurations (
                            {selectedYear.gradesCount} grades)
                          </div>
                        </div>
                      </label>
                    </div>

                    <div className="flex items-center space-x-2">
                      <Checkbox
                        id="import-subjects"
                        checked={importOptions.importSubjects}
                        onCheckedChange={(checked) =>
                          setImportOptions((prev) => ({
                            ...prev,
                            importSubjects: checked as boolean,
                          }))
                        }
                      />
                      <label
                        htmlFor="import-subjects"
                        className="flex items-center gap-2 cursor-pointer"
                      >
                        <BookOpen className="h-4 w-4" />
                        <div>
                          <div className="font-medium">Import Subjects</div>
                          <div className="text-sm text-gray-600">
                            Import all subjects and their assignments (
                            {selectedYear.subjectsCount} subjects)
                          </div>
                        </div>
                      </label>
                    </div>
                  </CardContent>
                </Card>

                {/* Warning */}
                <Card className="bg-amber-50 border-amber-200">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-2">
                      <AlertCircle className="h-5 w-5 text-amber-600 mt-0.5" />
                      <div>
                        <h4 className="font-medium text-amber-800">
                          Import Notice
                        </h4>
                        <p className="text-sm text-amber-700 mt-1">
                          Importing data will replace your current
                          configuration.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Action Buttons */}
            <DialogFooter className="sticky bottom-0 bg-white border-t p-4 z-10">
              <div className="ml-auto flex gap-3">
                <Button variant="outline" onClick={() => setIsOpen(false)}>
                  Cancel
                </Button>
                <Button
                  onClick={handleImport}
                  disabled={
                    !selectedYear ||
                    (!importOptions.importGrades &&
                      !importOptions.importSubjects)
                  }
                >
                  <Download className="h-4 w-4 mr-2" />
                  Import Selected Data
                </Button>
              </div>
            </DialogFooter>
          </div>
        ) : (
          /* Import Progress */
          <div className="space-y-6 py-8">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin mx-auto text-blue-500 mb-4" />
              <h3 className="text-lg font-medium mb-2">
                Importing Academic Year Data
              </h3>
              <p className="text-gray-600">
                Importing from {selectedYear?.name}
              </p>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span>{importStep}</span>
                <span>{Math.round(importProgress)}%</span>
              </div>
              <Progress value={importProgress} className="h-2" />
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}
