import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from '@/components/ui/table';
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import { Badge } from '@/components/ui/badge';
import { toast } from "sonner"
import { AdminHeader, AdminPanel } from '@/components/layout';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { CalendarIcon } from "lucide-react"
import { format } from "date-fns"
import { EventTable } from '@/features/admin/tables';
import { adminApi } from '@/api';

export default function AdminManageEvent() {
    const [semesters, setSemesters] = useState([]);
    const [selectedSemester, setSelectedSemester] = useState(null);
    const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
    const [isDialogOpen, setIsDialogOpen] = useState(false);

    // Mock initial data
    useEffect(() => {

        const fetchEvents = async () => {
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
        }

        fetchEvents();
    }, []);

    const getStatus = (start, end) => {
        const now = new Date();
        if (now > end) return 'closed';
        if (now >= start && now <= end) return 'open';
        return 'upcoming';
    };

    const handleSubmit = async (event) => {
        if (selectedSemester) {
            setSemesters(semesters.map(s => s.id === event.id ? event : s));
            toast({ title: 'Semester updated successfully' });
        } else {
            try {
                const response = await adminApi.createRegistrationEvent(event);
                if (response.status === 201) {
                    setSemesters([...semesters, response.data]);
                    const currentTime = new Date().toLocaleString("en-US", {
                        weekday: "long",
                        year: "numeric",
                        month: "long",
                        day: "2-digit",
                        hour: "numeric",
                        minute: "2-digit",
                        hour12: true,
                    });
                    toast.success(response.data['message'], {
                        description: currentTime,
                        style: { color: 'green' }
                    });
                }
            } catch (error) {
                if (error.response && error.response.data && error.response.data['error']) {
                    console.log(error.response.data['error'])
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
            setSemesters([...semesters, { ...event, id: Date.now().toString() }]);
            toast({ title: 'New semester announced' });
        }
        setIsDialogOpen(false);
    };

    const handleDelete = () => {
        setSemesters(semesters.filter(s => s.id !== selectedSemester?.id));
        setIsDeleteDialogOpen(false);
        toast({ title: 'Semester deleted successfully' });
    };

    return (
        <div className="min-h-screen flex overflow-hidden flex-col">
            <AdminHeader />
            <div className="flex flex-1 scroll-m-0">
                <AdminPanel />
                <div className="p-8 flex-1 mt-[4.6rem] ml-[11rem] bg-gray-100">
                    <div className="flex justify-between items-center mb-8">
                        <h1 className="text-3xl font-bold">Semester Registration Management</h1>
                        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                            <DialogTrigger asChild>
                                <Button>Create New Semester</Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[600px]">
                                <DialogHeader>
                                    <DialogTitle>
                                        {selectedSemester ? 'Edit Semester' : 'Create New Semester'}
                                    </DialogTitle>
                                </DialogHeader>
                                <PopoverForm
                                    initialData={selectedSemester}
                                    onSubmit={handleSubmit}
                                    onCancel={() => setIsDialogOpen(false)}
                                />
                            </DialogContent>
                        </Dialog>
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
                </div>
            </div>
        </div>
    );
}

function PopoverForm({ initialData, onSubmit, onCancel }) {
    const [formData, setFormData] = useState(initialData || {
        id: '',
        name: null,
        academicYearEC: null,
        startDate: new Date(),
        endDate: new Date(),
        registrationStart: new Date(),
        registrationEnd: new Date(),
        status: 'upcoming'
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <Tabs defaultValue="registration" className="space-y-6">
            <TabsList>
                <TabsTrigger value="registration">Registration Window</TabsTrigger>
                <TabsTrigger value="password">Password</TabsTrigger>
            </TabsList>
            <TabsContent value="registration">
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid grid-cols-2 gap-6">
                        <div className="space-y-2">
                            <Label>Semester</Label>
                            <Select
                                onValueChange={(value) => setFormData({ ...formData, name: parseFloat(value) })}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Semester" />
                                </SelectTrigger>
                                <SelectContent>
                                    {Array.from({ length: 2 }, (_, i) => i + 1).map(semester =>
                                        <SelectItem key={semester} value={`${semester}`}>
                                            Semester {semester}
                                        </SelectItem>
                                    )}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="academicYear">Academic Year</Label>
                            <Input
                                id="academicYear"
                                type="number"
                                value={formData.academicYearEC}
                                onChange={(e) => setFormData({ ...formData, academicYearEC: parseFloat(e.target.value) })}
                                required
                            />
                        </div>
                        <div>
                            <Label>Semester Start Date</Label>
                            <Popover modal={true}>
                                <PopoverTrigger asChild>
                                    <Button
                                        variant={"outline"}
                                        className={cn(
                                            "w-[280px] justify-start text-left font-normal",
                                            !formData.startDate && "text-muted-foreground"
                                        )}
                                    >
                                        <CalendarIcon className="mr-2 h-4 w-4" />
                                        {formData.startDate ? format(formData.startDate, "PPP") : <span>Pick a date</span>}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent className="w-auto p-0">
                                    <Calendar
                                        mode="single"
                                        selected={formData.startDate}
                                        onSelect={(date) => date && setFormData({ ...formData, startDate: date })}
                                        initialFocus
                                    />
                                </PopoverContent>
                            </Popover>
                        </div>
                        <div>
                            <Label>Semester End Date</Label>
                            <Popover modal={true}>
                                <PopoverTrigger asChild>
                                    <Button
                                        variant={"outline"}
                                        className={cn(
                                            "w-[280px] justify-start text-left font-normal",
                                            !formData.endDate && "text-muted-foreground"
                                        )}
                                    >
                                        <CalendarIcon className="mr-2 h-4 w-4" />
                                        {formData.endDate ? format(formData.endDate, "PPP") : <span>Pick a date</span>}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent className="w-auto p-0">
                                    <Calendar
                                        mode="single"
                                        selected={formData.endDate}
                                        onSelect={(date) => date && setFormData({ ...formData, endDate: date })}
                                        initialFocus
                                    />
                                </PopoverContent>
                            </Popover>
                        </div>
                        <div>
                            <Label>Registration Window Start Date</Label>
                            <Popover modal={true}>
                                <PopoverTrigger asChild>
                                    <Button
                                        variant={"outline"}
                                        className={cn(
                                            "w-[280px] justify-start text-left font-normal",
                                            !formData.registrationStart && "text-muted-foreground"
                                        )}
                                    >
                                        <CalendarIcon className="mr-2 h-4 w-4" />
                                        {formData.registrationStart ? format(formData.registrationStart, "PPP") : <span>Pick a date</span>}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent className="w-auto p-0">
                                    <Calendar
                                        mode="single"
                                        selected={formData.registrationStart}
                                        onSelect={(date) => date && setFormData({ ...formData, registrationStart: date })}
                                        initialFocus
                                    />
                                </PopoverContent>
                            </Popover>
                        </div>
                        <div>
                            <Label>Registration Window End Date</Label>
                            <Popover modal={true}>
                                <PopoverTrigger asChild>
                                    <Button
                                        variant={"outline"}
                                        className={cn(
                                            "w-[280px] justify-start text-left font-normal",
                                            !formData.registrationEnd && "text-muted-foreground"
                                        )}
                                    >
                                        <CalendarIcon className="mr-2 h-4 w-4" />
                                        {formData.registrationEnd ? format(formData.registrationEnd, "PPP") : <span>Pick a date</span>}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent className="w-auto p-0">
                                    <Calendar
                                        mode="single"
                                        selected={formData.registrationEnd}
                                        onSelect={(date) => date && setFormData({ ...formData, registrationEnd: date })}
                                        initialFocus
                                    />
                                </PopoverContent>
                            </Popover>
                        </div>
                    </div>

                    <div className="flex justify-end space-x-4">
                        <Button type="button" variant="outline" onClick={onCancel}>
                            Cancel
                        </Button>
                        <Button type="submit">
                            {initialData ? 'Update Semester' : 'Create Semester'}
                        </Button>
                    </div>
                </form>
            </TabsContent>
        </Tabs >
    );
}
