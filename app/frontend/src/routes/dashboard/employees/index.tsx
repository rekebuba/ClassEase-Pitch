import { createFileRoute } from "@tanstack/react-router";

import { requireRoutePermission } from "@/lib/auth/route-guards";

export const Route = createFileRoute("/dashboard/employees/")({
  beforeLoad: () => requireRoutePermission(Permission["employees:read"]),
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/dashboard/employees/"!</div>;
}
