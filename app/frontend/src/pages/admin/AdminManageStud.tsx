import { Layout } from "@/components";
import { Shell } from "@/components/shell";
import { DataTableSkeleton } from "@/components/data-table";
import { Suspense } from "react"
import { Button } from "@/components/ui/button"
import { Plus } from "lucide-react"
import { StudentsTable, FeatureFlagsProvider } from "@/components/data-table/data-table-students"
import type { Student } from "@/lib/types"
import { useSearchParams, useNavigate } from "react-router-dom";
import { searchParamsCache, GetStudentsSchema } from "@/lib/validations";
import { getValidFilters } from "@/lib/data-table";
import { useUrlState } from "@/hooks/use-url-state";
import React from "react";
import { useQueryState } from "nuqs";

// Mock data and functions for demonstration
async function getStudentsData(input?: GetStudentsSchema) {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000))

  return {
    data: students,
    pageCount: 1,
  }
}

async function getStatusCounts() {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 800))

  return {
    active: 8,
    inactive: 2,
    suspended: 2,
  }
}

async function getGradeCounts() {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 600))

  return {
    9: 3,
    10: 3,
    11: 3,
    12: 3,
  }
}

async function getAttendanceRange() {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 500))

  return [65, 98] as [number, number]
}

async function getGradeRange() {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 400))

  return [65, 94] as [number, number]
}

const students: Student[] = [
  {
    id: "1",
    name: "Emma Johnson",
    email: "emma.j@example.com",
    grade: 10,
    section: "A",
    status: "active",
    attendance: 95,
    averageGrade: 88,
    parentName: "Michael Johnson",
    parentEmail: "michael.j@example.com",
    joinedDate: "Sep 2, 2022",
  },
  {
    id: "2",
    name: "Liam Smith",
    email: "liam.s@example.com",
    grade: 9,
    section: "B",
    status: "active",
    attendance: 92,
    averageGrade: 76,
    parentName: "Sarah Smith",
    parentEmail: "sarah.s@example.com",
    joinedDate: "Aug 15, 2022",
  },
  {
    id: "3",
    name: "Olivia Brown",
    email: "olivia.b@example.com",
    grade: 11,
    section: "A",
    status: "inactive",
    attendance: 78,
    averageGrade: 91,
    parentName: "David Brown",
    parentEmail: "david.b@example.com",
    joinedDate: "Sep 5, 2021",
  },
  {
    id: "4",
    name: "Noah Davis",
    email: "noah.d@example.com",
    grade: 12,
    section: "C",
    status: "active",
    attendance: 98,
    averageGrade: 94,
    parentName: "Jennifer Davis",
    parentEmail: "jennifer.d@example.com",
    joinedDate: "Aug 20, 2020",
  },
  {
    id: "5",
    name: "Ava Wilson",
    email: "ava.w@example.com",
    grade: 10,
    section: "B",
    status: "suspended",
    attendance: 65,
    averageGrade: 72,
    parentName: "Robert Wilson",
    parentEmail: "robert.w@example.com",
    joinedDate: "Sep 1, 2022",
  },
  {
    id: "6",
    name: "Sophia Martinez",
    email: "sophia.m@example.com",
    grade: 9,
    section: "A",
    status: "active",
    attendance: 90,
    averageGrade: 85,
    parentName: "Maria Martinez",
    parentEmail: "maria.m@example.com",
    joinedDate: "Aug 25, 2022",
  },
  {
    id: "7",
    name: "Jackson Anderson",
    email: "jackson.a@example.com",
    grade: 11,
    section: "C",
    status: "active",
    attendance: 93,
    averageGrade: 89,
    parentName: "Thomas Anderson",
    parentEmail: "thomas.a@example.com",
    joinedDate: "Sep 3, 2021",
  },
  {
    id: "8",
    name: "Isabella Taylor",
    email: "isabella.t@example.com",
    grade: 12,
    section: "B",
    status: "inactive",
    attendance: 82,
    averageGrade: 79,
    parentName: "Patricia Taylor",
    parentEmail: "patricia.t@example.com",
    joinedDate: "Aug 18, 2020",
  },
  {
    id: "9",
    name: "Lucas Thomas",
    email: "lucas.t@example.com",
    grade: 10,
    section: "A",
    status: "active",
    attendance: 96,
    averageGrade: 92,
    parentName: "Christopher Thomas",
    parentEmail: "christopher.t@example.com",
    joinedDate: "Sep 7, 2022",
  },
  {
    id: "10",
    name: "Mia Harris",
    email: "mia.h@example.com",
    grade: 9,
    section: "C",
    status: "active",
    attendance: 91,
    averageGrade: 84,
    parentName: "Elizabeth Harris",
    parentEmail: "elizabeth.h@example.com",
    joinedDate: "Aug 22, 2022",
  },
  {
    id: "11",
    name: "Ethan Clark",
    email: "ethan.c@example.com",
    grade: 11,
    section: "B",
    status: "active",
    attendance: 94,
    averageGrade: 87,
    parentName: "Daniel Clark",
    parentEmail: "daniel.c@example.com",
    joinedDate: "Sep 4, 2021",
  },
  {
    id: "12",
    name: "Charlotte Lewis",
    email: "charlotte.l@example.com",
    grade: 12,
    section: "A",
    status: "suspended",
    attendance: 68,
    averageGrade: 65,
    parentName: "Richard Lewis",
    parentEmail: "richard.l@example.com",
    joinedDate: "Aug 19, 2020",
  },
]
interface SearchParams {
  [key: string]: string | string[] | undefined;
}
interface IndexPageProps {
  searchParams: Promise<SearchParams>;
}

const AdminManageStudents = () => {
  // const [search, setSearch] = useQueryState('search')

  // React.useEffect(() => {
  //   console.log('Query changed:', search)
  // }, [search])

  // const search = searchParamsCache.parse(Object.fromEntries(searchParams.entries()));
  // useEffect(() => {
  //   // setSearchParams(search);
  // }, [searchParams])
  // const validFilters = getValidFilters(search.filters);

  const promises = [
    getStudentsData(),
    getStatusCounts(),
    getGradeCounts(),
    getAttendanceRange(),
    getGradeRange()
  ];

  return (
    <Layout role="admin">

      <div className="container mx-auto py-5">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Students</h1>
            <p className="text-muted-foreground">
              Manage student information, track performance, and handle enrollments.
            </p>
          </div>
          <Button>
            <Plus className="mr-2 h-4 w-4" /> Add Student
          </Button>
        </div>
        <Shell className="gap-2">
          <FeatureFlagsProvider>
            <Suspense
              fallback={
                <DataTableSkeleton
                  columnCount={7}
                  filterCount={2}
                  cellWidths={[
                    "10rem",
                    "30rem",
                    "10rem",
                    "10rem",
                    "6rem",
                    "6rem",
                    "6rem",
                  ]}
                  shrinkZero
                />
              }>
              <StudentsTable
                promises={promises}
              />
            </Suspense>
          </FeatureFlagsProvider>
        </Shell>

      </div>
    </Layout>
  );
};

export default AdminManageStudents;
