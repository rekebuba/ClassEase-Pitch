import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/settings/grades/")({
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/settings/grades/"!</div>;
}
