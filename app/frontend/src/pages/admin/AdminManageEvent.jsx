import { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { toast } from "sonner"
import { AdminLayout } from '@/components/layout';
import { EventTable } from '@/features/admin/tables';
import { adminApi } from '@/api';
import { useNavigate } from 'react-router-dom';

export default function AdminManageEvent() {
    const [semesters, setSemesters] = useState([]);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const navigate = useNavigate();

    const fetchEvents = useCallback(async () => {
        try {
            const response = await adminApi.getEvents();
            if (response.status === 200) setSemesters(response.data);
        } catch (error) {
            if (error.response && error.response.data && error.response.data['error']) {
                toast.error(error.response.data['error'], {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            } else {
                toast.error("An unexpected error occurred.", {
                    description: "Please try again later, if the problem persists, contact the administrator.",
                    style: { color: 'red' }
                });
            }
        }
    }, []);
    // Mock initial data
    useEffect(() => {
        fetchEvents();
    }, [fetchEvents]);


    const handleDelete = () => {
        setIsDeleteDialogOpen(false);
        toast({ title: 'Semester deleted successfully' });
    };

    const goToEventForm = () => {
        navigate('/admin/event/new');
    }

    return (
        <AdminLayout>
            <div className="flex justify-between items-center p-5">
                <h1 className="text-3xl font-bold">List of Events</h1>
                <Button onClick={goToEventForm}>Create New Event</Button>
                {/* <PopoverForm
                            initialData={selectedSemester}
                            onSubmit={handleSubmit}
                            onCancel={() => setIsDialogOpen(false)}
                        /> */}
            </div>
            <EventTable events={semesters} />
            {/* Delete Confirmation Dialog */}
            <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Confirm Deletion</DialogTitle>
                        <DialogDescription>
                            Are you sure you want to delete this semester? This action cannot be undone.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="flex justify-end space-x-4">
                        <Button variant="outline" onClick={() => setIsDeleteDialogOpen(false)}>
                            Cancel
                        </Button>
                        <Button variant="destructive" onClick={handleDelete}>
                            Confirm Delete
                        </Button>
                    </div>
                </DialogContent>
            </Dialog>
        </AdminLayout>
    );
}
