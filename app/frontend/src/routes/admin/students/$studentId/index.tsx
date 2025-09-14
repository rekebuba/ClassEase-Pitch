import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/admin/students/$studentId/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/admin/students/$studentId/"!</div>;
}
