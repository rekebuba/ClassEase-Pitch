import { createFileRoute } from "@tanstack/react-router";
import { Search } from "lucide-react";
import { useMemo, useState } from "react";

import { SchoolCard } from "@/components/guest/school-card";
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
import { Skeleton } from "@/components/ui/skeleton";
import { guestSchools } from "@/lib/guest-data";

export const Route = createFileRoute("/guest/schools/")({
  component: SchoolsPage,
});

function SchoolsPage() {
  const [query, setQuery] = useState("");
  const [location, setLocation] = useState("all");
  const [category, setCategory] = useState("all");
  const [availability, setAvailability] = useState("open");
  const [loading, setLoading] = useState(false);

  const locations = [...new Set(guestSchools.map(school => school.city))];
  const categories = [...new Set(guestSchools.flatMap(school => school.positions.map(position => position.category)))];

  const schools = useMemo(() => {
    const normalized = query.trim().toLowerCase();

    return guestSchools.filter((school) => {
      const positionText = school.positions.map(position => `${position.title} ${position.category}`).join(" ");
      const matchesQuery = !normalized
        || `${school.name} ${school.location} ${school.category} ${positionText}`.toLowerCase().includes(normalized);
      const matchesLocation = location === "all" || school.city === location;
      const matchesCategory = category === "all" || school.positions.some(position => position.category === category);
      const matchesAvailability = availability === "all"
        || (availability === "open" ? school.applicationsOpen : !school.applicationsOpen);

      return matchesQuery && matchesLocation && matchesCategory && matchesAvailability;
    });
  }, [availability, category, location, query]);

  function updateSearch(value: string) {
    setQuery(value);
    setLoading(true);
    window.setTimeout(() => setLoading(false), 250);
  }

  return (
    <div className="space-y-6">
      <section className="rounded-xl border bg-background p-6 sm:p-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl space-y-2">
            <Badge variant="secondary">School discovery</Badge>
            <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Find schools accepting applications</h1>
            <p className="text-muted-foreground">
              Search by school, location, or position. Your saved profile will be reused when you apply.
            </p>
          </div>
          <div className="text-sm text-muted-foreground">
            {schools.length}
            {" "}
            result
            {schools.length === 1 ? "" : "s"}
          </div>
        </div>
      </section>

      <section className="grid gap-3 rounded-lg border bg-background p-4 md:grid-cols-[1fr_180px_180px_180px]">
        <div className="relative">
          <Search className="absolute left-3 top-2.5 size-4 text-muted-foreground" />
          <Input
            value={query}
            onChange={event => updateSearch(event.target.value)}
            placeholder="Search schools or positions..."
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
        <Select value={availability} onValueChange={setAvailability}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Availability" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="open">Applications open</SelectItem>
            <SelectItem value="closed">Closed</SelectItem>
            <SelectItem value="all">All schools</SelectItem>
          </SelectContent>
        </Select>
      </section>

      {loading
        ? (
            <div className="grid gap-4 lg:grid-cols-2">
              <Skeleton className="h-72 rounded-lg" />
              <Skeleton className="h-72 rounded-lg" />
            </div>
          )
        : schools.length > 0
          ? (
              <div className="grid gap-4 lg:grid-cols-2">
                {schools.map(school => <SchoolCard key={school.slug} school={school} />)}
              </div>
            )
          : (
              <Empty className="border bg-background">
                <EmptyHeader>
                  <EmptyMedia variant="icon">
                    <Search />
                  </EmptyMedia>
                  <EmptyTitle>No schools found</EmptyTitle>
                  <EmptyDescription>Try a different position, location, or availability filter.</EmptyDescription>
                </EmptyHeader>
              </Empty>
            )}
    </div>
  );
}
