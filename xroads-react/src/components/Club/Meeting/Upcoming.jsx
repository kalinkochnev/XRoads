import React, { useEffect, useState } from 'react';
import moment from "moment";
import { date } from 'yup';

const isToday = (otherDate) => {
    if (typeof otherDate == "string") {
        otherDate = new Date(Date.parse(otherDate));
    }
    const today = new Date()
    return otherDate.getDate() == today.getDate() &&
        otherDate.getMonth() == today.getMonth() &&
        otherDate.getFullYear() == today.getFullYear()
}

const UpcomingEvents = ({events = []}) => {
    const [sortedEvents, setEvents] = useState(null);
    let weekdayName = (dateObj) => moment(dateObj).format('dddd')
    let strToTime = (timeStr) => moment(timeStr, "H:mm:ss").toDate();

    const setup = () => {
        // Setup events object
        let unordered = {};
        for (var event of events) {
            let eventDate = moment(event.date, 'yyyy-MM-DD').toDate()

            if (Array.isArray(unordered[eventDate])) {
                unordered[eventDate].push(event)  
            } else {
                unordered[eventDate] = [event];
            }
        }
        return unordered
    }
    
    const sortEvents = (unorderedEvents) => {
        // Sort object by date
        let orderedEvents = {};
        Object.keys(unorderedEvents).sort((d1, d2) => {
            return Date.parse(d1) - Date.parse(d2)
        }).forEach(date => {
            orderedEvents[date] = unorderedEvents[date];
        })
        // For each date, sort events by start time
        for (var date of Object.keys(orderedEvents)) {
            orderedEvents[date].sort((e1, e2) => {
                return strToTime(e1.start) - strToTime(e2.start);
            })
        }
        return orderedEvents;
    }
    
    useEffect(() => {
        let events = sortEvents(setup());
        setEvents(events);
    }, [events]);


    return (
        <div>
            <p>Events</p>
            { sortedEvents ? Object.keys(sortedEvents).map(date => {
                return (
                    <div>
                        <b>{isToday(date) ? "Today's meetings" : weekdayName(date)}</b>
                        { sortedEvents[date].map(event => {
                            return (<p>{event.name}</p>)
                        })}
                    </div>
                );
            }) : null}
        </div>
    );
}

export default UpcomingEvents;
