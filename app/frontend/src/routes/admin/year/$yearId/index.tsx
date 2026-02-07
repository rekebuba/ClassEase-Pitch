import { useQuery } from "@tanstack/react-query";
import { createFileRoute, useLocation } from "@tanstack/react-router";
import { ArrowLeft, Calendar, Search } from "lucide-react";
import z from "zod";

import {
  getGradesSetupOptions,
  getSubjectsSetupOptions,
  getYearByIdOptions,
} from "@/client/@tanstack/react-query.gen";
import {
  DetailGradeCard,
  DetailSubjectCard,
  YearStatusBadge,
} from "@/components/academic-year";
import { ApiState } from "@/components/api-state";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { formatDate } from "@/lib/format";
import { queryClient } from "@/lib/query-client";

export const Route = createFileRoute("/admin/year/$yearId/")({
  validateSearch: z.object({ q: z.string().optional() }),
  loaderDeps: ({ search }) => ({ q: search?.q }),
  component: RouteComponent,
  loader: async ({ params, deps: { q } }) => {
    const hash = location.hash?.replace("#", "grades");
    await queryClient.ensureQueryData(
      getYearByIdOptions({ path: { year_id: params.yearId } }),
    );
    if (hash === "grades") {
      await queryClient.ensureQueryData(
        getGradesSetupOptions({
          query: { yearId: params.yearId, q },
        }),
      );
    }
    else if (hash === "subjects") {
      await queryClient.ensureQueryData(
        getSubjectsSetupOptions({
          query: { yearId: params.yearId, q },
        }),
      );
    }
  },
});

export default function RouteComponent() {
  const yearId = Route.useParams().yearId!;
  const { q: filter } = Route.useSearch();
  const navigate = Route.useNavigate();
  const location = useLocation();
  const { data: year } = useQuery(
    getYearByIdOptions({ path: { year_id: yearId } }),
  );

  // default to grades if no hash
  const activeTab = location.hash?.replace("#", "") || "grades";

  function handleSearchChange(e: React.ChangeEvent<HTMLInputElement>) {
    navigate({
      search: prev => ({ ...prev, q: e.target.value }),
      hash: activeTab,
    });
  }

  const {
    data: grades,
    isLoading: isGradesLoading,
    error: isGradesError,
  } = useQuery({
    ...getGradesSetupOptions({
      query: { yearId, q: filter || "" },
    }),
    enabled: activeTab === "grades",
  });

  const {
    data: subjects,
    isLoading: isSubjectsLoading,
    error: isSubjectsError,
  } = useQuery({
    ...getSubjectsSetupOptions({
      query: { yearId, q: filter || "" },
    }),
    enabled: activeTab === "subjects",
  });

  if (!year)
    return <div>Loading...</div>;

  const getDuration = () => {
    const start = new Date(year.startDate);
    const end = new Date(year.endDate);
    const diffTime = Math.abs(end.getTime() - start.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return `${diffDays} days`;
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate({ to: "/admin/year", params: { yearId } })}
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{year.name}</h1>
            <div className="flex items-center gap-3 mt-1">
              <YearStatusBadge status={year.status} />
              <span className="text-sm text-gray-600">
                {formatDate(year.startDate)}
                {" "}
                -
                {formatDate(year.endDate)}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Basic Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Calendar className="h-5 w-5" />
            Basic Information
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium text-sm text-gray-600 mb-1">
                Academic Year
              </h4>
              <p className="font-medium">{year.name}</p>
            </div>
            <div>
              <h4 className="font-medium text-sm text-gray-600 mb-1">
                Duration
              </h4>
              <p className="font-medium">{getDuration()}</p>
            </div>
            <div>
              <h4 className="font-medium text-sm text-gray-600 mb-1">
                Term System
              </h4>
              <p className="font-medium capitalize">{year.calendarType}</p>
            </div>
            <div>
              <h4 className="font-medium text-sm text-gray-600 mb-1">
                Start Date
              </h4>
              <p className="font-medium">{formatDate(year.startDate)}</p>
            </div>
            <div>
              <h4 className="font-medium text-sm text-gray-600 mb-1">
                End Date
              </h4>
              <p className="font-medium">{formatDate(year.endDate)}</p>
            </div>
            <div>
              <h4 className="font-medium text-sm text-gray-600 mb-1">Status</h4>
              <YearStatusBadge status={year.status} />
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex-1">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search ..."
            value={filter || ""}
            onChange={handleSearchChange}
            className="pl-10"
          />
        </div>
      </div>
      <Tabs
        defaultValue="grades"
        value={activeTab}
        onValueChange={value => navigate({ hash: value })}
        className="w-full"
      >
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="grades">Grades</TabsTrigger>
          <TabsTrigger value="subjects">Subjects</TabsTrigger>
        </TabsList>
        <TabsContent value="grades" className="flex-1 mt-5">
          <ApiState isLoading={isGradesLoading} error={isGradesError?.message}>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {grades?.map(grade => (
                <DetailGradeCard
                  key={grade.id}
                  grade={grade}
                  subjects={grade.subjects}
                >
                </DetailGradeCard>
              ))}
            </div>
          </ApiState>
        </TabsContent>
        <TabsContent value="subjects" className="flex-1 mt-5">
          <ApiState
            isLoading={isSubjectsLoading}
            error={isSubjectsError?.message}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {subjects?.map(subject => (
                <DetailSubjectCard
                  key={subject.id}
                  subject={subject}
                  grades={subject.grades}
                >
                </DetailSubjectCard>
              ))}
            </div>
          </ApiState>
        </TabsContent>
      </Tabs>

      {/* Metadata */}
      <Card>
        <CardHeader>
          <CardTitle>Configuration History</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Created:</span>
              <div className="font-medium">{formatDate(year.createdAt)}</div>
            </div>
            <div>
              <span className="text-gray-600">Last Updated:</span>
              <div className="font-medium">{formatDate(year.updatedAt)}</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
