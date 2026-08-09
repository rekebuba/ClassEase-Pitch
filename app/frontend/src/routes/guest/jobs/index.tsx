import { createFileRoute } from "@tanstack/react-router";
import { BriefcaseBusiness, Search } from "lucide-react";
import { useMemo, useState } from "react";

import { PositionCard } from "@/components/guest/position-card";
import { Badge } from "@/components/ui/badge";
import { Empty, EmptyDescription, EmptyHeader, EmptyMedia, EmptyTitle } from "@/components/ui/empty";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { getOpenPositions, isPositionAcceptingApplications } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/jobs/")({
  component: JobsPage,
});

function JobsPage() {
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("all");
  const [category, setCategory] = useState("all");
  const [employmentType, setEmploymentType] = useState("all");
  const allPositions = useMemo(() => getOpenPositions(), []);

  const locations = [...new Set(allPositions.map(({ position }) => position.location))];
  const categories = [...new Set(allPositions.map(({ position }) => position.category))];
  const employmentTypes = [...new Set(allPositions.map(({ position }) => position.employmentType))];

  const positions = useMemo(() => {
    const normalized = query.trim().toLowerCase();

    return allPositions.filter(({ school, position }) => {
      const searchText = `${position.title} ${position.summary} ${school.name} ${school.location} ${position.category}`;
      const matchesQuery = !normalized || searchText.toLowerCase().includes(normalized);
      const matchesLocation = location === "all" || position.location === location;
      const matchesCategory = category === "all" || position.category === category;
      const matchesType = employmentType === "all" || position.employmentType === employmentType;

      return matchesQuery && matchesLocation && matchesCategory && matchesType;
    });
  }, [allPositions, category, employmentType, location, query]);

  const openCount = positions.filter(({ position }) => isPositionAcceptingApplications(position)).length;

  return (
    <div className="space-y-6">
      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl space-y-2">
            <Badge variant="secondary">Employment</Badge>
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Find a Position</h1>
            <p className="text-muted-foreground">
              Explore schools currently hiring teachers, administrators, and staff.
            </p>
          </div>
          <div className="text-sm text-muted-foreground">
            {openCount}
            {" "}
            open position
            {openCount === 1 ? "" : "s"}
          </div>
        </div>
      </section>

      <section className="grid gap-3 rounded-lg border bg-background p-4 md:grid-cols-[1fr_180px_180px_180px]">
        <div className="relative">
          <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
          <Input
            value={query}
            onChange={event => setQuery(event.target.value)}
            placeholder="Search positions..."
            className="pl-9"
          />
        </div>
        <Select value={location} onValueChange={setLocation}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Location" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All locations</SelectItem>
            {locations.map(item => <SelectItem key={item} value={item}>{item}</SelectItem>)}
          </SelectContent>
        </Select>
        <Select value={category} onValueChange={setCategory}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All categories</SelectItem>
            {categories.map(item => <SelectItem key={item} value={item}>{item}</SelectItem>)}
          </SelectContent>
        </Select>
        <Select value={employmentType} onValueChange={setEmploymentType}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Employment type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All types</SelectItem>
            {employmentTypes.map(item => <SelectItem key={item} value={item}>{item}</SelectItem>)}
          </SelectContent>
        </Select>
      </section>

      {positions.length > 0
        ? (
            <div className="grid gap-4">
              {positions.map(({ school, position }) => (
                <PositionCard key={`${school.slug}-${position.id}`} school={school} schoolSlug={school.slug} position={position} />
              ))}
            </div>
          )
        : (
            <Empty className="border bg-background">
              <EmptyHeader>
                <EmptyMedia variant="icon">
                  <BriefcaseBusiness />
                </EmptyMedia>
                <EmptyTitle>No positions found</EmptyTitle>
                <EmptyDescription>Try a different search, location, category, or employment type.</EmptyDescription>
              </EmptyHeader>
            </Empty>
          )}
    </div>
  );
}
