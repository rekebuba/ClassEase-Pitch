import {
  deleteYearMutation,
  getYearsOptions,
  getYearSummaryOptions,
  getYearSummaryQueryKey,
  postYearMutation,
} from "@/client/@tanstack/react-query.gen";
import { NewYear, YearSummary } from "@/client/types.gen";
import { zAcademicTermTypeEnum, zNewYear } from "@/client/zod.gen";
import { ApiState } from "@/components/api-state";
import { yearColumns } from "@/components/data-table/year/columns";
import { YearTable } from "@/components/data-table/year/year-table";
import { DateWithLabel } from "@/components/inputs/date-labeled";
import { InputWithLabel } from "@/components/inputs/input-labeled";
import { RadioGroupLabel } from "@/components/inputs/radio-group-labeled";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";
import { academicYearRange } from "@/utils/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute } from "@tanstack/react-router";
import { Filter, Loader, Plus, Search } from "lucide-react";
import { useEffect, useState } from "react";
import {
  FormProvider,
  SubmitHandler,
  useForm,
  UseFormReturn,
} from "react-hook-form";
import { toast } from "sonner";
import z from "zod";

export const Route = createFileRoute("/admin/year/")({
  validateSearch: z.object({ q: z.string().optional() }),
  loaderDeps: ({ search }) => ({ q: search?.q }),
  loader: async ({ deps: { q } }) => {
    await queryClient.ensureQueryData(
      getYearSummaryOptions({
        query: { q: q },
      }),
    );
  },
  component: RouteComponent,
});

function RouteComponent() {
  const { q: searchTerm } = Route.useSearch();
  const navigate = Route.useNavigate();
  const [formDialogOpen, setFormDialogOpen] = useState(false);
  const [statusFilter, setStatusFilter] = useState<string>("all");

  const getYearQueryConfig = () => ({
    query: { q: searchTerm || "" },
  });

  const {
    data: years,
    isLoading: isYearsLoading,
    isError: isYearsError,
  } = useQuery(getYearSummaryOptions(getYearQueryConfig()));

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    navigate({
      search: (prev) => ({ ...prev, q: e.target.value }),
    });
  }

  const [defaultValues] = useState<NewYear>({
    name: "",
    calendarType: "Semester",
    status: "active",
    startDate: "",
    endDate: "",
    setupMethods: "Last Year Copy",
    copyFromYearId: null,
  });

  const newYearForm = useForm<NewYear>({
    resolver: zodResolver(zNewYear),
    defaultValues,
  });

  const newYearMutation = useMutation({
    ...postYearMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getYearSummaryQueryKey(getYearQueryConfig()),
      });
      queryClient.invalidateQueries({
        queryKey: getYearsOptions().queryKey,
      });

      newYearForm.reset(defaultValues);
      setFormDialogOpen(false);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          newYearForm.setError(field as keyof NewYear, {
            type: "server",
            message: message as string,
          });
        });
      }
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const deleteYear = useMutation({
    ...deleteYearMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getYearSummaryQueryKey(getYearQueryConfig()),
      });
      queryClient.invalidateQueries({
        queryKey: getYearsOptions().queryKey,
      });
    },
    onError: () => {
      toast.error("Something went wrong.", { style: { color: "red" } });
    },
  });

  const submitNewYear: SubmitHandler<NewYear> = (data) => {
    newYearMutation.mutate({
      body: data,
    });
  };

  const handleView = (yearId: string) => {
    navigate({ to: "/admin/year/$yearId", params: { yearId } });
  };

  const handleDelete = (yearId: string) => {
    deleteYear.mutate({ path: { year_id: yearId } });
  };

  // Main list view
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Academic Year Management
            </h1>
            <p className="text-gray-600 mt-1">
              Manage and configure your school's academic years
            </p>
          </div>
          <AlertDialog open={formDialogOpen} onOpenChange={setFormDialogOpen}>
            <AlertDialogTrigger asChild>
              <Button variant="default">
                <Plus className="h-4 w-4 mr-2" />
                Add New Year
              </Button>
            </AlertDialogTrigger>

            <FormDialog
              newYearForm={newYearForm}
              submitNewYear={submitNewYear}
              isNewYearPending={newYearMutation.isPending}
            />
          </AlertDialog>
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
                    onChange={handleSearchChange}
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
          <ApiState
            isLoading={isYearsLoading}
            error={isYearsError ? "Failed to load academic years." : undefined}
          >
            <YearTable<YearSummary>
              columns={yearColumns(handleView, handleDelete)}
              data={years || []}
            />
          </ApiState>
        </Card>
      </div>
    </div>
  );
}

function FormDialog({
  newYearForm,
  submitNewYear,
  isNewYearPending,
}: {
  newYearForm: UseFormReturn<NewYear>;
  submitNewYear: (data: NewYear) => void;
  isNewYearPending: boolean;
}) {
  const currentYear = store.getState().year;
  const {
    watch,
    formState: { isDirty },
    handleSubmit,
  } = newYearForm;

  const watchForm = watch();

  useEffect(() => {
    if (watchForm.setupMethods !== "Last Year Copy") {
      newYearForm.setValue("copyFromYearId", null, {
        shouldDirty: true,
        shouldValidate: true,
      });
    } else if (watchForm.setupMethods === "Last Year Copy") {
      newYearForm.setValue("copyFromYearId", currentYear.id, {
        shouldDirty: true,
        shouldValidate: true,
      });
    }
  }, [watchForm.setupMethods, currentYear.id, newYearForm]);

  // Form submission
  const handleSave = handleSubmit(submitNewYear);

  return (
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Create New Academic Year</AlertDialogTitle>
        <AlertDialogDescription>
          Fill out the details below. Required fields are marked with *
        </AlertDialogDescription>
      </AlertDialogHeader>
      <FormProvider {...newYearForm}>
        <div className="space-y-6 pt-4 border-t">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <InputWithLabel<NewYear>
              fieldTitle="Academic Year Name"
              nameInSchema="name"
              placeholder="e.g., 2024-2025 Academic Year"
            />
            <SelectWithLabel<NewYear, string>
              fieldTitle="Term System"
              nameInSchema="calendarType"
            >
              {zAcademicTermTypeEnum.options.map((option) => (
                <SelectItem value={option}>{option}</SelectItem>
              ))}
            </SelectWithLabel>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <DateWithLabel<NewYear>
              fieldTitle="Academic Year Start Date"
              nameInSchema="startDate"
            />
            <DateWithLabel<NewYear>
              fieldTitle="Academic Year End Date"
              nameInSchema="endDate"
              className="flex-1 min-w-0"
              disableFrom={
                watchForm.startDate
                  ? new Date(watchForm.startDate)
                  : new Date("1900-01-01")
              }
            />
          </div>
          <RadioGroupLabel<NewYear, NewYear["setupMethods"]>
            fieldTitle="Choose a method"
            nameInSchema="setupMethods"
            options={[
              {
                label: `Current Year Copy ${academicYearRange(currentYear.startDate, currentYear.endDate)} (Recommended)`,
                value: "Last Year Copy",
              },
              {
                label: "Default Template - If You do Not Have Previous Data",
                value: "Default Template",
              },
              { label: "Manual Setup", value: "Manual" },
            ]}
          />
        </div>

        {/* Action Buttons */}
        <AlertDialogFooter className="mt-5">
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button
              disabled={!isDirty || isNewYearPending}
              type="submit"
              onClick={handleSave}
              className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed w-32"
            >
              {isNewYearPending && (
                <Loader className="animate-spin mr-2 h-4 w-4" />
              )}
              Save Changes
            </Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </FormProvider>
    </AlertDialogContent>
  );
}
