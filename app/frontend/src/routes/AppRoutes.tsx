import { createBrowserRouter } from "react-router-dom";
import { LandingPage, AuthPage } from "@/pages";
import { Forbidden, NotFound, ServerError, ServiceUnavailablePage } from "@/pages/error"
import {
    AdminDashboard,
    AdminCreateMarkList,
    AdminEnrollUser,
    AdminManageEvent,
    AdminManageStudents,
    AdminManageTeacher,
    AdminUpdateProfile,
    AdminUserAccessControl,
    AdminEventForm,
    ManageTeachersApplication,
    ManageStudentsApplication
} from "@/pages/admin";
import {
    TeacherDashboard,
    TeacherManageStudent,
    TeacherUpdateProfile
} from "@/pages/teacher";
import {
    StudentDashboard,
    StudentUpdateProfile,
    StudentRegistrationForm,
    StudentReportCard,
    StudentCourseRegistration
} from "@/pages/student";
import { ProtectedRoute } from "@/routes";


/**
 * Defines the routes for the application using `createBrowserRouter`.
 */
const router = createBrowserRouter([
    {
        path: "/",
        element: <LandingPage />,
        errorElement: <NotFound />,
    },
    {
        path: "/forbidden",
        element: <Forbidden />,
        loader: () => ({ status: 403, statusText: "Forbidden" }),
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
        element: <AuthPage />,
    },
    {
        path: "/admin/dashboard",
        element: <ProtectedRoute element={<AdminDashboard />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/manage/students",
        element: <ProtectedRoute element={<AdminManageStudents />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/manage/teachers",
        element: <ProtectedRoute element={<AdminManageTeacher />} allowedRoles={['admin']} />,
    },
    {
        path: "admin/student/registration",
        element: <AdminEnrollUser role="student" />
    },
    {
        path: "/admin/assessment/mark-list",
        element: <ProtectedRoute element={<AdminCreateMarkList />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/calendar/events",
        element: <ProtectedRoute element={<AdminManageEvent />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/manage/user-access",
        element: <ProtectedRoute element={<AdminUserAccessControl />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/update/profile",
        element: <ProtectedRoute element={<AdminUpdateProfile />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/student/applications",
        element: <ManageStudentsApplication />
    },
    {
        path: "/admin/student/registration/new",
        element: <ProtectedRoute element={<AdminEnrollUser role="student" />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/teacher/applications",
        element: <ManageTeachersApplication />
    },
    {
        path: "/admin/teacher/registration/new",
        element: <ProtectedRoute element={<AdminEnrollUser role="teacher" />} allowedRoles={['admin']} />,
    },
    {
        path: '/admin/event/new',
        element: <ProtectedRoute element={<AdminEventForm />} allowedRoles={['admin']} />,
    },
    {
        path: "/teacher/dashboard",
        element: <ProtectedRoute element={<TeacherDashboard />} allowedRoles={['teacher']} />,
    },
    {
        path: "/teacher/students",
        element: <ProtectedRoute element={<TeacherManageStudent />} allowedRoles={['teacher']} />
    },
    {
        path: "/teacher/update/profile",
        element: <ProtectedRoute element={<TeacherUpdateProfile />} allowedRoles={['teacher']} />,
    },
    {
        path: "/student/dashboard",
        element: <ProtectedRoute element={<StudentDashboard />} allowedRoles={['student']} />,
    },
    {
        path: "/student/registration",
        element: <ProtectedRoute element={<StudentRegistrationForm />} allowedRoles={['admin']} />,
    },
    {
        path: "/student/course/registration",
        element: <ProtectedRoute element={<StudentCourseRegistration />} allowedRoles={['student']} />,
    },
    {
        path: "/student/update/profile",
        element: <ProtectedRoute element={<StudentUpdateProfile />} allowedRoles={['student']} />
    },
    {
        path: "/student/report-card",
        element: <ProtectedRoute element={<StudentReportCard />} allowedRoles={['student']} />
    }
]);

export default router;
