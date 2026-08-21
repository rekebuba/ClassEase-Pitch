import { createFileRoute } from "@tanstack/react-router";
import { FileArchive } from "lucide-react";
import { useMemo, useState } from "react";

import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { HRPageHeader, HRStatCard, MockActionDialog, SectionCard, StatusBadge } from "@/features/hr/components/common";
import { documents } from "@/features/hr/data/mock";

export const Route = createFileRoute("/dashboard/hr/documents/")({
  component: HRDocumentsPage,
});

function HRDocumentsPage() {
  const [search, setSearch] = useState("");
  const filtered = useMemo(() => {
    const term = search.toLowerCase();
    return documents.filter(document => [document.name, document.employee, document.category, document.status].some(value => value.toLowerCase().includes(term)));
  }, [search]);

  return (
    <div className="space-y-6">
      <HRPageHeader title="Employee Documents" description="Document status, expiration dates, and verification workflow." actions={<MockActionDialog label="Mock Upload" title="Upload document" description="No backend upload is performed." />} />
      <div className="grid gap-4 md:grid-cols-4">
        <HRStatCard title="Documents" value={String(documents.length)} detail="Mock records" icon={FileArchive} />
        <HRStatCard title="Expiring Soon" value="1" detail="Needs staff follow-up" icon={FileArchive} />
        <HRStatCard title="Expired" value="1" detail="Requires update" icon={FileArchive} />
        <HRStatCard title="Pending Verification" value="1" detail="HR review queue" icon={FileArchive} />
      </div>
      <SectionCard title="Document Register">
        <Input value={search} onChange={event => setSearch(event.target.value)} placeholder="Search documents..." className="mb-4 max-w-sm" />
        <div className="overflow-hidden rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Document</TableHead>
                <TableHead>Employee</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Upload Date</TableHead>
                <TableHead>Expiration Date</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.map(document => (
                <TableRow key={document.id}>
                  <TableCell className="font-medium">{document.name}</TableCell>
                  <TableCell>{document.employee}</TableCell>
                  <TableCell>{document.category}</TableCell>
                  <TableCell>{document.uploadDate}</TableCell>
                  <TableCell>{document.expirationDate ?? "N/A"}</TableCell>
                  <TableCell><StatusBadge value={document.status} /></TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </SectionCard>
    </div>
  );
}
