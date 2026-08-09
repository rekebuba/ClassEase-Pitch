import { createFileRoute, Navigate, notFound } from "@tanstack/react-router";

import { getOpenPositions } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/jobs/$positionId/")({
  component: JobAliasPage,
});

function JobAliasPage() {
  const { positionId } = Route.useParams();
  const match = getOpenPositions().find(({ position }) => position.id === positionId);

  if (!match) {
    throw notFound();
  }

  return (
    <Navigate
      to="/guest/schools/$schoolSlug/positions/$positionId"
      params={{ schoolSlug: match.school.slug, positionId: match.position.id }}
      replace
    />
  );
}
