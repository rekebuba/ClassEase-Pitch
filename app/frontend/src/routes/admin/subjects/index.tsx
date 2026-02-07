import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import { createFileRoute, Link } from "@tanstack/react-router";
import { BookOpen, Edit, Loader, Plus, Search } from "lucide-react";
import { useState } from "react";
import {
  FormProvider,
  useForm,
} from "react-hook-form";
import { toast } from "sonner";

import {
  getSubjectsSetupOptions,
  getSubjectsSetupQueryKey,
  postSubjectMutation,
} from "@/client/@tanstack/react-query.gen";
import { zGetSubjectsSetupData, zNewSubject } from "@/client/zod.gen";
import DetailSubjectCard from "@/components/academic-year/detail-subject-card";
import { ApiState } from "@/components/api-state";
import { InputWithLabel } from "@/components/inputs/input-labeled";
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
import { Textarea } from "@/components/ui/textarea";
import { queryClient } from "@/lib/query-client";
import { store } from "@/store/main-store";

import type { NewSubject } from "@/client/types.gen";
import type {
  SubmitHandler,
  UseFormReturn,
} from "react-hook-form";

const zSearch = zGetSubjectsSetupData.shape.query.pick({ q: true });

export const Route = createFileRoute("/admin/subjects/")({
  validateSearch: zSearch,
  loaderDeps: ({ search }) => ({ q: search?.q }),
  loader: async ({ deps: { q } }) => {
    const yearId = store.getState().year.id;
    if (yearId) {
      await queryClient.ensureQueryData(
        getSubjectsSetupOptions({
          query: { yearId, q },
        }),
      );
    }
  },
  component: RouteComponent,
});

function RouteComponent() {
  const yearId = store.getState().year.id;
  const { q: filterSubject } = Route.useSearch();
  const navigate = Route.useNavigate();
  const [formDialogOpen, setFormDialogOpen] = useState(false);

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    navigate({
      search: prev => ({ ...prev, q: e.target.value }),
    });
  }

  const getSubjectsQueryConfig = () => ({
    query: { yearId: yearId!, q: filterSubject || "" },
  });

  const {
    data: subjects,
    isLoading,
    error,
  } = useQuery(getSubjectsSetupOptions(getSubjectsQueryConfig()));

  const [defaultValues] = useState<NewSubject>({
    yearId: yearId || "",
    name: "",
    code: "",
  });

  const newSubjectForm = useForm<NewSubject>({
    resolver: zodResolver(zNewSubject),
    defaultValues,
  });

  const newSubjectMutation = useMutation({
    ...postSubjectMutation(),
    onSuccess: (success) => {
      toast.success(success.message, {
        style: { color: "green" },
      });
      queryClient.invalidateQueries({
        queryKey: getSubjectsSetupQueryKey(getSubjectsQueryConfig()),
      });
      newSubjectForm.reset(defaultValues);
      setFormDialogOpen(false);
    },
    onError: (error: any) => {
      const detail = error.response?.data?.detail;

      if (detail && typeof detail === "object") {
        Object.entries(detail).forEach(([field, message]) => {
          newSubjectForm.setError(field as keyof NewSubject, {
            type: "server",
            message: message as string,
          });
        });
      }
      else {
        toast.error("Something went wrong. Please try again.");
      }
    },
  });

  const submitNewSubject: SubmitHandler<NewSubject> = (data) => {
    newSubjectMutation.mutate({
      body: data,
    });
  };

  return (
    <Card>
      <CardHeader className="pb-4">
        <CardTitle className="text-xl font-semibold">
          Subject Management
        </CardTitle>
        <p className="text-sm text-gray-500">
          Configure subjects for your School
        </p>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Search & Add */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Search subjects..."
                value={filterSubject || ""}
                onChange={handleSearchChange}
                className="pl-10"
              />
            </div>
          </div>
          <AlertDialog open={formDialogOpen} onOpenChange={setFormDialogOpen}>
            <AlertDialogTrigger asChild>
              <Button variant="default">
                <Plus className="h-4 w-4 mr-2" />
                Add New Subject
              </Button>
            </AlertDialogTrigger>

            <FormDialog
              newSubjectForm={newSubjectForm}
              submitNewSubject={submitNewSubject}
              isNewSubjectPending={newSubjectMutation.isPending}
            />
          </AlertDialog>
        </div>

        <ApiState isLoading={isLoading} error={error?.message}>
          {/* Empty State */}
          {subjects?.length === 0 && (
            <EmptyState
              hasSubjects={subjects.length > 0}
              searchTerm={filterSubject || ""}
            />
          )}

          {/* Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {subjects?.map(subject => (
              <DetailSubjectCard
                key={subject.id}
                subject={subject}
                grades={subject.grades}
              >
                <div className="flex gap-2 mt-4">
                  <Button
                    asChild
                    variant="outline"
                    size="sm"
                    className="flex-1 border-gray-300 hover:bg-blue-50"
                  >
                    <Link
                      to="/admin/subjects/$subjectId"
                      params={{ subjectId: subject.id }}
                    >
                      <Edit className="h-4 w-4 mr-1" />
                      Edit
                    </Link>
                  </Button>
                </div>
              </DetailSubjectCard>
            ))}
          </div>
        </ApiState>
      </CardContent>
    </Card>
  );
}

function EmptyState({
  hasSubjects,
  searchTerm,
}: {
  hasSubjects: boolean;
  searchTerm: string;
}) {
  return (
    <div className="text-center py-12 text-gray-500">
      <BookOpen className="h-12 w-12 mx-auto mb-4 opacity-50" />
      <p>
        {hasSubjects && searchTerm !== ""
          ? `No subjects match "${searchTerm}"`
          : "No subjects added yet. Add your first grade above."}
      </p>
    </div>
  );
}

function FormDialog({
  newSubjectForm,
  submitNewSubject,
  isNewSubjectPending,
}: {
  newSubjectForm: UseFormReturn<NewSubject>;
  submitNewSubject: (data: NewSubject) => void;
  isNewSubjectPending: boolean;
}) {
  const {
    formState: { isDirty },
    handleSubmit,
  } = newSubjectForm;

  // Form submission
  const handleSave = handleSubmit(submitNewSubject);

  return (
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle>Create New Subject</AlertDialogTitle>
        <AlertDialogDescription>
          Fill out the details below to add a new subject. Required fields are
          marked with *
        </AlertDialogDescription>
      </AlertDialogHeader>
      <FormProvider {...newSubjectForm}>
        <div className="space-y-6 pt-4 border-t">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <InputWithLabel<NewSubject>
                fieldTitle="Subject Name *"
                nameInSchema="name"
                placeholder="e.g., Mathematics"
              />
            </div>
            <div>
              <InputWithLabel<NewSubject>
                fieldTitle="Subject Code *"
                nameInSchema="code"
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
        </div>

        {/* Action Buttons */}
        <AlertDialogFooter className="mt-5">
          <AlertDialogCancel>Cancel</AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button
              disabled={!isDirty || isNewSubjectPending}
              type="submit"
              onClick={handleSave}
              className="bg-blue-600 text-white hover:bg-blue-700 disabled:pointer-events-auto disabled:cursor-not-allowed w-32"
            >
              {isNewSubjectPending && (
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
