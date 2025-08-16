import {
  ApiHandlerResponse,
  QueryParams,
  renameViewData,
  SearchParams,
  StudentsViews,
  View,
} from "@/lib/types";
import { api, zodApiHandler } from "@/api";
import { toast } from "sonner";
import {
  ApiResponse,
  AverageRangeSchema,
  GradeCountsSchema,
  SectionCountSchema,
  StatusCountSchema,
  StudentsDataSchema,
  StudentsViewSchema,
} from "@/lib/validations";
import { z } from "zod";
import qs from "qs";
import { create } from "domain";
import {
  DetailTeacherAPPlicationSchema,
  TeacherApplicationSchema,
} from "@/lib/api-validation";
import { buildQueryParams } from "@/utils/build-query-params";

export const adminApi = {
  getUser: <T extends z.ZodObject<any>>(
    userId: string,
    schema: T,
    params?: QueryParams,
  ): Promise<ApiHandlerResponse<z.infer<T>>> => {
    return zodApiHandler(
      () =>
        api.get(`/users/${userId}/admin`, { params: buildQueryParams(params) }),
      schema,
    );
  },
  getDashboardData: () => api.get("/admin/dashboard"),
  getSchoolOverview: () => api.get("/admin/overview"),
  getStudents: (validQuery: SearchParams) =>
    api.post("/admin/students", validQuery),
  getStudentsStatusCounts: () => api.get("/admin/students/status-count"),
  getStudentsAverageRange: () => api.get("/admin/students/average-range"),
  getGradeCounts: () => api.get("/admin/students/grade-counts"),
  getSectionCounts: () => api.get("/admin/students/section-counts"),
  getAllStudentsViews: () => api.get("/admin/all-views/students"),
  createNewView: (viewData: View) => api.post("/admin/views", viewData),
  updateView: (updatedView: StudentsViews) =>
    api.put("/admin/update-view", updatedView),
  renameView: (renameView: renameViewData) =>
    api.put("/admin/rename-view", renameView),
  deleteView: (viewId: string) => api.put(`/admin/delete-view/${viewId}`),
  getTeachers: () => api.get("/admin/teachers"),
  createUser: (userData) => api.post("/admin/users", userData),
  createMarkList: (markListData) =>
    api.post("/admin/students/mark_list", markListData),
  assignTeacher: (requirements) =>
    api.post("/admin/assign-teacher", requirements),
  updateProfile: (userData) => api.put("/admin/profile", userData),
  deleteUser: (userId) => api.delete(`/admin/users/${userId}`),
  createEvent: (eventData) => api.post("/admin/event/new", eventData),
  getEvents: () => api.get("/admin/events"),
  fetchTeachersApplications: () => api.get("/admin/teacher/applications"),
  detailTeachersApplications: (applicationId: string) =>
    api.get(`/admin/teacher/applications/${applicationId}`),
  updateTeacherApplicationStatus: (applicationId: string, newStatus: string) =>
    api.put(`/admin/teacher/applications/${applicationId}`, {
      status: newStatus,
    }),
};

export const getStudents = async (validQuery: SearchParams) => {
  const response = await zodApiHandler(
    () => adminApi.getStudents(validQuery),
    StudentsDataSchema,
  );

  if (!response.success) {
    throw new Error("Failed to fetch students data", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const getStudentsStatusCounts = async () => {
  const response = await zodApiHandler(
    () => adminApi.getStudentsStatusCounts(),
    StatusCountSchema,
  );

  if (!response.success) {
    console.error(response.error.details);
    throw new Error("Failed to fetch students status counts", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const getStudentsAverageRange = async () => {
  const response = await zodApiHandler(
    () => adminApi.getStudentsAverageRange(),
    AverageRangeSchema,
  );

  if (!response.success) {
    throw new Error("Failed to fetch students grade counts", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const getGradeCounts = async () => {
  const response = await zodApiHandler(
    () => adminApi.getGradeCounts(),
    GradeCountsSchema,
  );

  if (!response.success) {
    console.error(response.error.details);
    throw new Error("Failed to fetch students grade counts", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const getSectionCounts = async () => {
  const response = await zodApiHandler(
    () => adminApi.getSectionCounts(),
    SectionCountSchema,
  );

  if (!response.success) {
    console.error(response.error.details);
    throw new Error("Failed to fetch students section counts", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const createNewView = async (newView: View) => {
  const response = await zodApiHandler(
    () => adminApi.createNewView(newView),
    ApiResponse,
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to Create view", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};
export const deleteView = async (viewId: string) => {
  const response = await zodApiHandler(
    () => adminApi.deleteView(viewId),
    ApiResponse,
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to Delete view", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const renameView = async (newView: renameViewData) => {
  const response = await zodApiHandler(
    () => adminApi.renameView(newView),
    ApiResponse,
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to Rename view", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const getAllStudentsViews = async () => {
  const response = await zodApiHandler(
    () => adminApi.getAllStudentsViews(),
    StudentsViewSchema.array(),
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to fetch students views", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const updateView = async (updatedView: StudentsViews) => {
  const response = await zodApiHandler(
    () => adminApi.updateView(updatedView),
    ApiResponse,
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to update students view", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const fetchTeachersApplications = async () => {
  const response = await zodApiHandler(
    () => adminApi.fetchTeachersApplications(),
    TeacherApplicationSchema.array(),
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to fetch teachers applications", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const detailTeachersApplications = async (applicationId: string) => {
  const response = await zodApiHandler(
    () => adminApi.detailTeachersApplications(applicationId),
    DetailTeacherAPPlicationSchema,
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to fetch teacher application details", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};

export const updateTeacherApplicationStatus = async (
  applicationId: string,
  newStatus: string,
) => {
  const response = await zodApiHandler(
    () => adminApi.updateTeacherApplicationStatus(applicationId, newStatus),
    ApiResponse,
  );

  if (!response.success) {
    toast.error(response.error.message, {
      style: { color: "red" },
    });
    console.error(response.error.details);
    throw new Error("Failed to update teacher application status", {
      cause: JSON.stringify(response.error.details),
    });
  }

  return response.data;
};
