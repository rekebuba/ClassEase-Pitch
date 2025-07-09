import { useState, useEffect, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Calendar } from '@/components/ui/calendar';
import { toast } from "sonner"
import { useNavigate } from 'react-router-dom';
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { CalendarIcon } from "lucide-react"
import { format } from "date-fns"
import { adminApi } from '@/api';

import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { Layout } from '@/components';


const EventForm = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        // id: '',

        // Section 1: Basic Event Information
        title: '',
        purpose: '',
        semester: {
            name: 0
        },
        organizer: '',

        // Section 2: Date & Time
        academicYear: 0,
        startDate: new Date(),
        endDate: new Date(),

        // Section 3: Event Location
        location: '',

        // Section 4: Participation & Registration
        requiresRegistration: false,
        registrationStart: new Date(),
        registrationEnd: new Date(),
        eligibility: 'All',
        hasFee: false,
        feeAmount: 0,

        // Section 5: Event Details
        description: '',
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formattedData = {
            ...formData,
            startDate: formData.startDate.toISOString().split('T')[0],
            endDate: formData.endDate.toISOString().split('T')[0],
            registrationStart: formData.registrationStart.toISOString().split('T')[0],
            registrationEnd: formData.registrationEnd.toISOString().split('T')[0],
        };
        try {
            const response = await adminApi.createEvent(formattedData);
            if (response.status === 201) {
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
                navigate('/admin/events')
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
    };


    return (
        <form onSubmit={handleSubmit} className="space-y-4 p-6 max-w-5xl mx-auto">
            <Card>
                <CardHeader>
                    <CardTitle>Event Purpose</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <Select
                            required
                            value={formData.purpose}
                            onValueChange={(value) => setFormData({ ...formData, purpose: value })}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Select purpose" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="New Semester">New Semester</SelectItem>
                                <SelectItem value="Academic">Academic</SelectItem>
                                <SelectItem value="Graduation">Graduation</SelectItem>
                                <SelectItem value="Administration">Administration</SelectItem>
                                <SelectItem value="other">Other</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>
            {/* Section 1: Basic Event Information */}
            {(formData.purpose && formData.purpose === 'New Semester') ?
                <div className="space-y-4">

                    <Card>
                        <CardHeader>
                            <CardTitle>Event Information</CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-2 gap-6">
                            <div className="space-y-4">
                                <Label>Event Name/Title</Label>
                                <Input
                                    required
                                    value={formData.title}
                                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                                />
                            </div>

                            <div className='space-y-4'>
                                <Label>Academic Year</Label>
                                <Select
                                    onValueChange={(value) => setFormData({ ...formData, academicYear: parseFloat(value) })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Ethiopian Academic Year" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="2017">Year 2017 (2024/25)</SelectItem>
                                        <SelectItem value="2016">Year 2016 (2023/24)</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="space-y-4">
                                <Label>Organizer</Label>
                                <Select
                                    value={formData.organizer}
                                    onValueChange={(value) => setFormData({ ...formData, organizer: value })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select organizer" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="School Administration">School Administration</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div className='space-y-4'>
                                <Label>Semester</Label>
                                <Select
                                    onValueChange={(value) => setFormData({ ...formData, semester: { name: parseFloat(value) } })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select semester" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="1">Semester 1</SelectItem>
                                        <SelectItem value="2">Semester 2</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Section 2: Date & Time */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Date & Time</CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-2 gap-6">
                            <div className="space-y-4 flex flex-col">
                                <Label>Start Date</Label>
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
                            <div className="space-y-4 flex flex-col">
                                <Label>End Date</Label>
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
                        </CardContent>
                        <CardContent className="flex flex-col gap-6">
                            <div className="flex flex-col gap-6">
                                <div className="flex items-center gap-2">
                                    <Label>Registration Required</Label>
                                    <Switch
                                        checked={formData.requiresRegistration}
                                        onCheckedChange={(checked) => setFormData({ ...formData, requiresRegistration: checked })}
                                    />
                                </div>
                                {formData.requiresRegistration && (
                                    <div className="grid grid-cols-2 gap-6">
                                        <div className="space-y-4 flex flex-col">
                                            <Label>Registration Starting Date</Label>
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
                                        <div className="space-y-4 flex flex-col ">
                                            <Label>Registration Deadline</Label>
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
                                )}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Section 3: Event Location */}
                    {/* {(formData.purpose && formData.purpose !== 'New Semester') && */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Event Location</CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-2 gap-6">
                            <div className="space-y-4">
                                <Label>Location Type</Label>
                                <Select
                                    value={formData.location}
                                    onValueChange={(value) => setFormData({ ...formData, location: value })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select location" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="Online">Online</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="flex flex-col gap-6">
                                <div className="flex items-center gap-2 mb-[-8px]">
                                    <Label>Has Fee</Label>
                                    <Switch
                                        checked={formData.hasFee}
                                        onCheckedChange={(checked) => setFormData({ ...formData, hasFee: checked })}
                                    />
                                </div>

                                {formData.hasFee && (
                                    <div className='grid grid-cols gap-6'>
                                        <div className="space-y-4">
                                            <Input
                                                type="number"
                                                min="300"
                                                value={formData.feeAmount}
                                                placeholder="Fee Amount"
                                                onChange={(e) => setFormData({ ...formData, feeAmount: parseFloat(e.target.value) })}
                                            />
                                        </div>
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                    {/* } */}

                    {/* Section 4: Event Details */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Event Details</CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-1 gap-6">
                            <div className="space-y-4">
                                <Label>Event Description</Label>
                                <Textarea
                                    value={formData.description}
                                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                                    rows={4}
                                />
                            </div>
                        </CardContent>
                    </Card>
                    <div className="flex justify-end space-x-4">
                        <Button type="submit">
                            Create Event
                        </Button>
                    </div>
                </div>
                :
                <></>
            }
        </form>
    );
}

export default EventForm;
