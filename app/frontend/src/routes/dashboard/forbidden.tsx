import { createFileRoute } from "@tanstack/react-router";

import { ForbiddenPage } from "@/components/errors/status-pages";

export const Route = createFileRoute("/dashboard/forbidden")({
  component: ForbiddenPage,
});
