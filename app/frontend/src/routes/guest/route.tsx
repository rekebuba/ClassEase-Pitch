import { createFileRoute } from "@tanstack/react-router";

import { GuestProvider } from "@/components/guest/guest-context";
import { GuestLayout } from "@/components/guest/guest-layout";

export const Route = createFileRoute("/guest")({
  // beforeLoad: requireGuest,
  component: RouteComponent,
});

function RouteComponent() {
  return (
    <GuestProvider>
      <GuestLayout />
    </GuestProvider>
  );
}
