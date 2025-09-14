import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/admin/students/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/admin/students/"!</div>;
}
