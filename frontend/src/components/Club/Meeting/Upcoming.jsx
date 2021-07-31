import React, { useEffect, useState } from 'react';
import moment from "moment";
import * as utils from "./utils";
import { Link } from "react-router-dom";

const UpcomingEvents = ({ events = [], displayedClubs = [], schoolSlug = "" }) => {
    const [sortedEvents, setEvents] = useState(null);
    let isHidden = (clubId) => !displayedClubs.map(club => club.id).includes(clubId)

    // This returns an event object which may have additional computed values,
    // Or be filtered out entirely and returns null. 
    const addEventAttrs = (event) => {

        event['clubObject'] = displayedClubs.filter(club => club.id == event.club)[0];
        event['school'] = schoolSlug;

        if (isHidden(event.club)) {
            return null;
        }
        return event;
    }

    const setup = () => {
        // Setup events object
        let unordered = {};
        for (var event of events) {
            let eventDate = moment(event.date, 'yyyy-MM-DD').toDate()
            event = addEventAttrs(event);
            if (event == null) {
                continue
            }

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
                return utils.strToTime(e1.start) - utils.strToTime(e2.start);
            })
        }
        return orderedEvents;
    }



    useEffect(() => {
        setEvents(sortEvents(setup()));
    }, [events, displayedClubs]);


    return (
        <div>
            {
                sortedEvents == null || Object.keys(sortedEvents).length == 0 &&
                <div className="no-results smaller">
                    <h1>╯︵╰</h1>
                    <h1 className="text">no events this week</h1>
                </div>
            }
            {sortedEvents ? Object.keys(sortedEvents).map(date => <DateComp date={date} events={sortedEvents[date]}></DateComp>) : null}
        </div>
    );
}

const DateComp = ({ date, events = [] }) => {
    return (
        <div>
            <h3>{utils.isToday(date) ? "Today's meetings" : utils.weekdayName(date)}</h3>
            {events.map(event => <Event event={event}></Event>)}
        </div>
    );
}

const Event = ({ event }) => {
    let startTime = utils.timeObjToStr(utils.strToTime(event.start));
    return (
        <div>
            <Link className="discrete-link" to={`/${event.school}/${event.clubObject.slug}`}>
                <p>{startTime} · {event.clubObject.name}</p>
            </Link>
        </div>
    )
}

export default UpcomingEvents;
