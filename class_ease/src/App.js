import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from './pages/NotFound';
import AdminDashboard from "./pages/AdminDashboard";
import ProtectedRoute from "./ProtectedRoute";
import TeacherDashboard from "./pages/TeachDashbord";
import StudentDashboard from "./pages/StudDashbord";
import StudentRegistrationForm from "./pages/StudRegistrationForm";
import AdminManageStudents from "./pages/AdminManageStud";
import AdminManageTeach from "./pages/AdminManageTeach";
import TeacherManageStudents from "./pages/TeacherManageStud";
import AdminCreateMarkList from "./pages/AdminMarkList";
import AdminEventManagement from "./pages/AdminEventManagement"
import AdminStudPerformance from "./pages/AdminStudPerformance";
import UserAccessControl from "./pages/AdminUsersAccessControl";
import AdminEnrollUser from "./pages/AdminEnrollUser";
import AssignTeacher from "./pages/AdminAssignTeacher";

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
    path: "/admin/manage/students",
    element: <AdminManageStudents />
  },
  {
    path: "/admin/manage/teachers",
    element: <AdminManageTeach />
  },
  {
    path: "/admin/assign/teachers",
    element: <AssignTeacher />
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
    element: <UserAccessControl />
  }
]);


function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
