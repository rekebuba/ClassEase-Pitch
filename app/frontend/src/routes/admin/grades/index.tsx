import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, Link } from "@tanstack/react-router";
import { Edit, GraduationCap, Loader, Plus, Search } from "lucide-react";
import { useMemo, useState } from "react";
import {
  FormProvider,
  useForm,
} from "react-hook-form";
import { toast } from "sonner";

import {
  getGradesSetupOptions,
  getGradesSetupQueryKey,
  postGradeMutation,
} from "@/client/@tanstack/react-query.gen";
import {
  zGetGradesSetupData,
  zGradeEnum,
  zGradeLevelEnum,
  zNewGrade,
} from "@/client/zod.gen";
import DetailGradeCard from "@/components/academic-year/detail-grade-card";
import { ApiState } from "@/components/api-state";
import { SelectWithLabel } from "@/components/inputs/select-labeled";
import { SwitchWithLabel } from "@/components/inputs/switch-labeled";
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
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { SelectItem } from "@/components/ui/select";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";

import type {
  GradeEnum,
  GradeLevelEnum,
  GradeSetupSchema,
  NewGrade,
} from "@/client/types.gen";
import type {
  SubmitHandler,
  UseFormReturn,
} from "react-hook-form";

const zSearch = zGetGradesSetupData.shape.query.pick({ q: true });

export const Route = createFileRoute("/admin/grades/")({
  validateSearch: zSearch,
  loaderDeps: ({ search }) => ({ q: search?.q }),
  loader: async ({ deps: { q } }) => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getGradesSetupOptions({
          query: { yearId, q },
        }),
      );
    }
  },
  component: RouteComponent,
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const { q: filterGrade } = Route.useSearch();
  const navigate = Route.useNavigate();
  const [formDialogOpen, setFormDialogOpen] = useState(false);

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    navigate({
      search: prev => ({ ...prev, q: e.target.value }),
    });
  }

  const getGradesQueryConfig = () => ({
    query: { yearId: yearId!, q: filterGrade || "" },
  });

  const {
    data: grades,
    isLoading,
    error,
  } = useQuery(getGradesSetupOptions(getGradesQueryConfig()));

  const [defaultValues] = useState<NewGrade>({
    yearId: yearId || "",
    grade: "" as GradeEnum,
    level: "" as GradeLevelEnum,
    hasStream: false,
  });

  const newGradeForm = useForm<NewGrade>({
    resolver: zodResolver(zNewGrade),
    defaultValues,
  });

  const newGradeMutation = useMutation({
    ...postGradeMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getGradesSetupQueryKey(getGradesQueryConfig()),
      });
      newGradeForm.reset(defaultValues);
      setFormDialogOpen(false);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          newGradeForm.setError(field as keyof NewGrade, {
            type: "server",
            message: message as string,
          });
        });
      }
      else {
        toast.error("Something went wrong. Please Check Your inputs.");
      }
    },
  });

  const submitNewGrade: SubmitHandler<NewGrade> = (data) => {
    newGradeMutation.mutate({
      body: data,
    });
  };

  return (
    <Card>
      <CardHeader className="pb-4">
        <CardTitle className="text-xl font-semibold">
          Grade Levels & Academic Streams
        </CardTitle>
        <p className="text-sm text-gray-500">
          Configure the grade levels and academic tracks for your school
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Search & Add */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search grades..."
                value={filterGrade || ""}
                onChange={handleSearchChange}
                className="pl-10"
              />
            </div>
          </div>
          <AlertDialog open={formDialogOpen} onOpenChange={setFormDialogOpen}>
            <AlertDialogTrigger asChild>
              <Button variant="default">
                <Plus className="h-4 w-4 mr-2" />
                Add New Grade
              </Button>
            </AlertDialogTrigger>

            <FormDialog
              newGradeForm={newGradeForm}
              submitNewGrade={submitNewGrade}
              grades={grades}
              isNewGradePending={newGradeMutation.isPending}
            />
          </AlertDialog>
        </div>
        <ApiState isLoading={isLoading} error={error?.message}>
          {/* Empty State */}
          {grades?.length === 0 && (
            <EmptyState
              hasGrades={grades.length > 0}
              searchTerm={filterGrade || ""}
            />
          )}

          {/* Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {grades?.map(grade => (
              <DetailGradeCard
                key={grade.id}
                grade={grade}
                subjects={grade.subjects}
              >
                <div className="flex gap-2 mt-4">
                  <Button
                    asChild
                    variant="outline"
                    size="sm"
                    className="flex-1 border-gray-300 hover:bg-blue-50"
                  >
                    <Link
                      to="/admin/grades/$gradeId"
                      params={{ gradeId: grade.id }}
                    >
                      <Edit className="h-4 w-4 mr-1" />
                      Edit
                    </Link>
                  </Button>
                </div>
              </DetailGradeCard>
            ))}
          </div>
        </ApiState>
      </CardContent>
    </Card>
  );
}

function EmptyState({
  hasGrades,
  searchTerm,
}: {
  hasGrades: boolean;
  searchTerm: string;
}) {
  return (
    <div className="text-center py-12 text-gray-500">
      <GraduationCap className="h-12 w-12 mx-auto mb-4 opacity-50" />
      <p>
        {hasGrades && searchTerm !== ""
          ? `No grades match "${searchTerm}"`
          : "No grades added yet. Add your first grade above."}
      </p>
    </div>
  );
}

function FormDialog({
  newGradeForm,
  submitNewGrade,
  grades,
  isNewGradePending,
}: {
  newGradeForm: UseFormReturn<NewGrade>;
  submitNewGrade: (data: NewGrade) => void;
  grades: GradeSetupSchema[] | undefined;
  isNewGradePending: boolean;
}) {
  const {
    formState: { isDirty },
    handleSubmit,
  } = newGradeForm;

  // Form submission
  const handleSave = handleSubmit(submitNewGrade);

  const availableGrades = useMemo(() => {
    // Filter out already selected grades
    return zGradeEnum.options.filter(
      gradeOption => !grades?.map(g => g.grade).includes(gradeOption),
    );
  }, [grades]);

  return (
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Create New Grade</AlertDialogTitle>
        <AlertDialogDescription>
          Fill out the details below to add a new Grade. Required fields are
          marked with *
        </AlertDialogDescription>
      </AlertDialogHeader>
      <FormProvider {...newGradeForm}>
        <div className="space-y-6 pt-4 border-t">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <SelectWithLabel<NewGrade, string>
                fieldTitle="Grade Name *"
                nameInSchema="grade"
              >
                {availableGrades.map(grade => (
                  <SelectItem key={grade} value={grade}>
                    Grade
                    {" "}
                    {grade}
                  </SelectItem>
                ))}
              </SelectWithLabel>
            </div>
            <div>
              <SelectWithLabel<NewGrade, string>
                fieldTitle="Grade Level *"
                nameInSchema="level"
              >
                {zGradeLevelEnum.options.map(level => (
                  <SelectItem key={level} value={level}>
                    {level}
                  </SelectItem>
                ))}
              </SelectWithLabel>
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <Label>Has Streams/Tracks</Label>
              <p className="text-sm text-gray-500">
                Enable different academic tracks for this grade
              </p>
            </div>
            <SwitchWithLabel fieldTitle="" nameInSchema="hasStream" />
          </div>
        </div>

        {/* Action Buttons */}
        <AlertDialogFooter className="mt-5">
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button
              disabled={!isDirty || isNewGradePending}
              type="submit"
              onClick={handleSave}
              className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed w-32"
            >
              {isNewGradePending && (
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
