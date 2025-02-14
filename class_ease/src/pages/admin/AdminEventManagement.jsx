import { useState } from 'react';
import { AdminHeader, AdminPanel } from "@/components/layout";


/**
 * 
 * @returns {JSX.Element} The rendered component.
 */
const EventManagement = () => {
    const [newEvent, setNewEvent] = useState({ title: '', description: '', date: '' });
    const [events, setEvents] = useState([]);

    const handleInputChange = (e) => {
        setNewEvent({ ...newEvent, [e.target.name]: e.target.value });
    };

    const addEvent = () => {
        setEvents([...events, newEvent]);
        setNewEvent({ title: '', description: '', date: '' }); // Reset the form fields
    };

    return (
        <div className="admin-manage-container">
            <AdminPanel />
            <main className="content">
                <AdminHeader />
                <h2>Event Management</h2>
                <div className="new-event-form">
                    <h3>Add New Event</h3>
                    <div className="new-event-group">
                        <label htmlFor="dob">Event Date: </label>
                        <input
                            type="date"
                            name="date"
                            value={newEvent.date}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <input
                        type="text"
                        name="title"
                        placeholder="Event Title"
                        value={newEvent.title}
                        onChange={handleInputChange}
                    />
                    <textarea
                        name="description"
                        placeholder="Event Description"
                        value={newEvent.description}
                        onChange={handleInputChange}
                    />
                    <button onClick={addEvent} disabled={!newEvent.date || !newEvent.title || !newEvent.description}>
                        Add Event
                    </button>
                </div>

                <h3>Upcoming Events</h3>
                <div className="new-event-list">
                    <ul>
                        {events.map((event, index) => (
                            <li key={index}>
                                <strong>{event.title}</strong> on {event.date}
                                <p>{event.description}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            </main>
        </div>
    );
};

export default EventManagement;
