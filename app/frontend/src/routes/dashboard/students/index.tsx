import { createFileRoute } from "@tanstack/react-router";

import { requireRoutePermission } from "@/lib/auth/route-guards";
import { Permission } from "@/lib/permissions";

export const Route = createFileRoute("/dashboard/students/")({
  beforeLoad: () => requireRoutePermission(Permission["students:read"]),
  component: RouteComponent,
});

function RouteComponent() {
  return <div>Hello "/dashboard/students/"!</div>;
}
