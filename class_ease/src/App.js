import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./components/Home";
import Login from "./services/Login";
import Logout from "./services/Logout";
import NotFound from './services/NotFound';
import AdminDashboard from "./pages/admin/AdminDashboard";
import ProtectedRoute from "./services/ProtectedRoute";
import TeacherDashboard from "./pages/teacher/TeacherDashboard";
import StudentDashboard from "./pages/student/StudentDashboard";
import StudentRegistrationForm from "./pages/student/StudentRegistrationForm";
import AdminManageStudents from "./pages/admin/AdminManageStudents";
import AdminManageTeach from "./pages/admin/AdminManageTeach";
import TeacherManageStudents from "./pages/teacher/TeacherManageStudents";
import AdminCreateMarkList from "./pages/admin/AdminCreateMarkList";
import AdminEventManagement from "./pages/admin/AdminEventManagement";
import AdminStudPerformance from "./pages/admin/AdminStudPerformance";
import AdminUserAccessControl from "./pages/admin/AdminUserAccessControl";
import AdminEnrollUser from "./pages/admin/AdminEnrollUser";
import AdminAssignTeacher from "./pages/admin/AdminAssignTeacher";
import TeacherUpdateProfile from "./pages/teacher/TeacherUpdateProfile";
import AdminUpdateProfile from "./pages/admin/AdminUpdateProfile";
import StudentUpdateProfile from "./pages/student/StudentUpdateProfile";

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
    path: "/logout",
    element: <Logout />,
  },
  {
    path: "/admin/dashboard",
    element: <AdminDashboard />
  },
  {
    path: "/teacher/dashboard",
    element: <ProtectedRoute element={<TeacherDashboard />} />,
  },
  {
    path: "/student/dashboard",
    element: <ProtectedRoute element={<StudentDashboard />} />,
  },
  {
    path: "/student/registration",
    element: <ProtectedRoute element={<StudentRegistrationForm />} />,
  },
  {
    path: "admin/student/registration",
    element: <AdminEnrollUser role="student" />
  },
  {
    path: "admin/teacher/registration",
    element: <AdminEnrollUser role="teacher" />
  },
  {
    path: "/teacher/update/profile",
    element: <ProtectedRoute element={<TeacherUpdateProfile />} />,
  },
  {
    path: "/admin/update/profile",
    element: <ProtectedRoute element={<AdminUpdateProfile />} />,
  },
  {
    path: "/student/update/profile",
    element: <ProtectedRoute element={<StudentUpdateProfile />} />
  },
  {
    path: "/admin/manage/students",
    element: <AdminManageStudents />
  },
  {
    path: "/admin/manage/teachers",
    element: <AdminManageTeach />
  },
  {
    path: "/admin/assign/teachers",
    element: <AdminAssignTeacher />
  },
  {
    path: "/teacher/students",
    element: <TeacherManageStudents />
  },
  {
    path: "/admin/assessment/marklist",
    element: <AdminCreateMarkList />
  },
  {
    path: "/admin/events/newevent",
    element: <AdminEventManagement />
  },
  {
    path: "/admin/students/performance",
    element: <AdminStudPerformance />
  },
  {
    path: "/admin/users/accesscontrol",
    element: <AdminUserAccessControl />
  }
]);


function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
