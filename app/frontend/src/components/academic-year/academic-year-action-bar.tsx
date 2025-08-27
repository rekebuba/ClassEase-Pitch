import { getYearsOptions } from "@/client/@tanstack/react-query.gen";
import {
  GetPreviousYearSetupData,
  YearWithRelatedSchema,
} from "@/client/types.gen";
import { zGetPreviousYearSetupData } from "@/client/zod.gen";
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
import {
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "@tanstack/react-router";
import {
  AlertCircle,
  BookOpen,
  CheckCircle,
  Download,
  GraduationCap,
  Save,
} from "lucide-react";
import { useState } from "react";
import { FormProvider, useForm } from "react-hook-form";

interface AcademicYearActionBarProps {
  mode: "create" | "edit";
  unsavedChanges: boolean;
}

export function AcademicYearActionBar({
  mode,
  unsavedChanges,
  onCancel,
}: AcademicYearActionBarProps) {
  const navigate = useNavigate();
  return (
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
        <Button
          variant="outline"
          onClick={() => navigate({ to: "/admin/years" })}
        >
          Cancel
        </Button>
        {mode === "create" && <ImportDataDialog />}
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
  );
}

type FormOptions = GetPreviousYearSetupData["query"];

export function ImportDataDialog() {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const { data: years, isLoading } = useQuery({
    ...getYearsOptions(),
    enabled: isOpen,
  });
  const [selectedYear, setSelectedYear] =
    useState<YearWithRelatedSchema | null>(null);
  const [defaultValues] = useState<FormOptions>({
    yearId: "",
    grades: false,
    subjects: false,
  });

  const form = useForm<FormOptions>({
    resolver: zodResolver(zGetPreviousYearSetupData.shape.query),
    defaultValues,
  });
  const {
    setValue,
    control,
    formState: { isDirty },
    handleSubmit,
  } = form;

  const getStatusColor = (status: YearWithRelatedSchema["status"]) => {
    switch (status) {
      case "completed":
        return "bg-green-100 text-green-800 border-green-200";
      case "active":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "upcoming":
        return "bg-gray-100 text-gray-800 border-gray-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  const onSubmit = (searchParams: FormOptions) => {
    console.log(searchParams);
    setIsOpen(false);
    navigate({ to: "/admin/years/new", search: searchParams, replace: true });
  };

  if (isLoading) return <div>loading...</div>;

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
        <FormProvider {...form}>
          <form
            onSubmit={handleSubmit(onSubmit)}
            className="overflow-y-auto px-4"
          >
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
                      onClick={() => {
                        setValue("yearId", year.id, { shouldDirty: true });
                        setSelectedYear(year);
                      }}
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
                                {year.grades.length} grades
                              </div>
                              <div className="flex items-center gap-1">
                                <BookOpen className="h-4 w-4" />
                                {year.subjects.length} subjects
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
                      <FormField
                        control={control}
                        name="grades"
                        render={({ field }) => (
                          <FormItem>
                            <div className="flex items-center space-x-2">
                              <FormControl>
                                <Checkbox
                                  onCheckedChange={field.onChange}
                                  checked={field.value}
                                />
                              </FormControl>
                              <label
                                htmlFor="import-grades"
                                className="flex items-center gap-2 cursor-pointer"
                              >
                                <GraduationCap className="h-4 w-4" />
                                <div>
                                  <div className="font-medium">
                                    Import Grades Structure
                                  </div>
                                  <FormDescription className="text-sm text-gray-600">
                                    Import all grade levels and their
                                    configurations ({selectedYear.grades.length}{" "}
                                    grades)
                                  </FormDescription>
                                </div>
                              </label>
                            </div>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                      <FormField
                        control={control}
                        name="subjects"
                        render={({ field }) => (
                          <FormItem>
                            <div className="flex items-center space-x-2">
                              <FormControl>
                                <Checkbox
                                  onCheckedChange={field.onChange}
                                  checked={field.value}
                                />
                              </FormControl>
                              <label
                                htmlFor="import-subjects"
                                className="flex items-center gap-2 cursor-pointer"
                              >
                                <BookOpen className="h-4 w-4" />
                                <div>
                                  <div className="font-medium">
                                    Import Subjects
                                  </div>
                                  <FormDescription className="text-sm text-gray-600">
                                    Import all subjects and their assignments (
                                    {selectedYear.subjects.length} subjects)
                                  </FormDescription>
                                </div>
                              </label>
                            </div>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </CardContent>
                  </Card>
                </div>
              )}

              {/* Warning */}
              <Card className="bg-amber-50 border-amber-200 mt-4">
                <CardContent className="p-4">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="h-5 w-5 text-amber-600 mt-0.5" />
                    <div>
                      <h4 className="font-medium text-amber-800">
                        Import Notice
                      </h4>
                      <p className="text-sm text-amber-700 mt-1">
                        Importing data will replace your current configuration.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              {/* Action Buttons */}
              <DialogFooter className="sticky bottom-0 bg-white border-t p-4 z-10">
                <div className="ml-auto flex gap-3">
                  <Button variant="outline" onClick={() => setIsOpen(false)}>
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={!isDirty}
                    className="hover:opacity-400"
                  >
                    <Download className="h-4 w-4 mr-2" />
                    Import Selected Data
                  </Button>
                </div>
              </DialogFooter>
            </div>
          </form>
        </FormProvider>
      </DialogContent>
    </Dialog>
  );
}
