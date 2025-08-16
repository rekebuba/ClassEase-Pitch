import { lazy } from "react";
import { createBrowserRouter, Navigate } from "react-router-dom";
import { AuthProvider } from "@/context/auth-context";
import { ProtectedRoute } from "@/routes/";
import { Layout } from "@/components";

// Error pages
const Forbidden = lazy(() => import("@/pages/error/403"));
const NotFound = lazy(() => import("@/pages/error/404"));
const ServerError = lazy(() => import("@/pages/error/500"));
const ServiceUnavailablePage = lazy(() => import("@/pages/error/503"));

// Auth pages
const AuthPage = lazy(() => import("@/pages/auth-page"));
const LandingPage = lazy(() => import("@/pages/landing-page"));

// Admin pages
const AdminDashboard = lazy(() => import("@/pages/admin/dashboard"));
const AcademicYearSetup = lazy(
  () => import("@/pages/admin/academic-year-setup"),
);
const AcademicYearManagement = lazy(
  () => import("@/pages/admin/academic-year-management"),
);
const AdminCreateMarkList = lazy(
  () => import("@/pages/admin/create-mark-list"),
);
const StudentRegistrationForm = lazy(
  () => import("@/pages/admin/student-registration-form"),
);
const TeacherRegistrationForm = lazy(
  () => import("@/pages/admin/teacher-registration-form"),
);
const AdminManageEvent = lazy(() => import("@/pages/admin/manage-event"));
const AdminManageStudents = lazy(() => import("@/pages/admin/manage-students"));
const AdminManageTeacher = lazy(() => import("@/pages/admin/manage-teachers"));
const AdminUpdateProfile = lazy(() => import("@/pages/admin/profile"));
const AdminUserAccessControl = lazy(
  () => import("@/pages/admin/user-access-control"),
);
const AdminEventForm = lazy(() => import("@/pages/admin/event-form"));
const ManageTeachersApplication = lazy(
  () => import("@/pages/admin/manage-teacher-application"),
);
const ManageStudentsApplication = lazy(
  () => import("@/pages/admin/manage-student-application"),
);

// Teacher pages
const TeacherDashboard = lazy(() => import("@/pages/teacher/dashboard"));
const TeacherManageStudent = lazy(
  () => import("@/pages/teacher/manage-student"),
);
const TeacherUpdateProfile = lazy(() => import("@/pages/teacher/profile"));

// Student pages
const StudentDashboard = lazy(() => import("@/pages/student/dashboard"));
const StudentUpdateProfile = lazy(() => import("@/pages/student/profile"));
const StudentReportCard = lazy(() => import("@/pages/student/report-card"));
const StudentCourseRegistration = lazy(
  () => import("@/pages/student/course-registration"),
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <LandingPage />,
    errorElement: <NotFound />,
  },
  {
    path: "/forbidden",
    element: <Forbidden />,
  },
  {
    path: "/server-error",
    element: <ServerError />,
  },
  {
    path: "/maintenance",
    element: <ServiceUnavailablePage />,
  },
  {
    path: "/auth",
    element: (
      <AuthProvider>
        <AuthPage />
      </AuthProvider>
    ),
  },
  {
    path: "/admin",
    element: (
      <AuthProvider>
        <Layout>
          <ProtectedRoute allowedRoles={["admin"]} />
        </Layout>
      </AuthProvider>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" replace /> },
      { path: "dashboard", element: <AdminDashboard /> },
      { path: "academic-year-setup", element: <AcademicYearSetup /> },
      { path: "academic-year-manage", element: <AcademicYearManagement /> },
      { path: "manage/students", element: <AdminManageStudents /> },
      { path: "manage/teachers", element: <AdminManageTeacher /> },
      { path: "student/registration", element: <StudentRegistrationForm /> },
      { path: "assessment/mark-list", element: <AdminCreateMarkList /> },
      { path: "calendar/events", element: <AdminManageEvent /> },
      { path: "manage/user-access", element: <AdminUserAccessControl /> },
      { path: "update/profile", element: <AdminUpdateProfile /> },
      { path: "student/applications", element: <ManageStudentsApplication /> },
      {
        path: "student/registration/new",
        element: <TeacherRegistrationForm />,
      },
      { path: "teacher/applications", element: <ManageTeachersApplication /> },
      {
        path: "teacher/registration/new",
        element: <TeacherRegistrationForm />,
      },
      { path: "event/new", element: <AdminEventForm /> },
    ],
  },
  {
    path: "/teacher",
    element: (
      <AuthProvider>
        <ProtectedRoute allowedRoles={["teacher"]} />
      </AuthProvider>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" replace /> },
      { path: "dashboard", element: <TeacherDashboard /> },
      { path: "students", element: <TeacherManageStudent /> },
      { path: "update/profile", element: <TeacherUpdateProfile /> },
    ],
  },
  {
    path: "/student",
    element: (
      <AuthProvider>
        <ProtectedRoute allowedRoles={["student"]} />
      </AuthProvider>
    ),
    children: [
      { index: true, element: <Navigate to="dashboard" replace /> },
      { path: "dashboard", element: <StudentDashboard /> },
      { path: "course/registration", element: <StudentCourseRegistration /> },
      { path: "update/profile", element: <StudentUpdateProfile /> },
      { path: "report-card", element: <StudentReportCard /> },
    ],
  },
]);

export default router;
