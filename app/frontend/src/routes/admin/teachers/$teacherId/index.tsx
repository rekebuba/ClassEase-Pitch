import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/admin/teachers/$teacherId/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/admin/teachers/$teacherId/"!</div>;
}
