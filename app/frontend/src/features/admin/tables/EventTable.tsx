import { eventColumn } from "./eventColumn";
import { DataTable } from "./data-table";

const EventTable = ({ events }) => {
  return (
    <div className="container mx-auto py-10">
      <DataTable columns={eventColumn} data={events} />
    </div>
  );
};

export default EventTable;
