import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";




import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from './pages/NotFound';
import AdminDashboard from "./pages/AdminDashboard";
import ProtectedRoute from "./ProtectedRoute";
import TeacherDashboard from "./pages/TeachDashbord";
import StudentDashboard from "./pages/StdDashbord";
import StudentRegistrationForm from "./pages/StudentRegistrationForm";


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
    element: <ProtectedRoute element={<AdminDashboard />} />,
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
  }
]);


function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
