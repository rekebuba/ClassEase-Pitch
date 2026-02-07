import { DataTable } from "./data-table";
import { eventColumn } from "./eventColumn";

function EventTable({ events }) {
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={eventColumn} data={events} />
    </div>
  );
}

export default EventTable;
