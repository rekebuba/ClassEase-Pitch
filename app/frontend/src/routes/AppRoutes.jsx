import { createBrowserRouter } from "react-router-dom";
import { Home, NotFound } from "@/pages/public";
import { Login } from "@/features/auth";
import {
    AdminDashboard,
    AdminCreateMarkList,
    AdminEnrollUser,
    AdminManageEvent,
    AdminManageStudents,
    AdminManageTeacher,
    AdminUpdateProfile,
    AdminUserAccessControl,
    AdminEventForm
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
        element: <Home />,
        errorElement: <NotFound />,
    },
    {
        path: "/login",
        element: <Login />,
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
        path: "/admin/assessment/marklist",
        element: <ProtectedRoute element={<AdminCreateMarkList />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/events",
        element: <ProtectedRoute element={<AdminManageEvent />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/users/accesscontrol",
        element: <ProtectedRoute element={<AdminUserAccessControl />} allowedRoles={['admin']} />,
    },
    {
        path: "/admin/update/profile",
        element: <ProtectedRoute element={<AdminUpdateProfile />} allowedRoles={['admin']} />,
    },
    {
        path: "admin/teacher/registration",
        element: <AdminEnrollUser role="teacher" />
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
