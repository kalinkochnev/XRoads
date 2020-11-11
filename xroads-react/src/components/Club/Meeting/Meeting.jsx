import React from "react";
const moment = require('moment');

const MeetingCard = ({ event }) => {
    let date_str = new Date(event.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'utc' });
    let start = formatTimeShow(event.start);
    let end = formatTimeShow(event.end);

    function formatTimeShow(time, includeSeconds=false, showMeridian=true) {
        let times = time.split(":") // hours, minutes, seconds
        
        for (let i = 0; i < 3; i++) {
            times[0] = Number(times[0])
        }

        var h = times[0] % 12;
        var m = times[1];
        var s = times[2];
        if (h === 0) h = 12;
        var meridian = (times[0] < 12 ? 'am' : 'pm');
        return (h < 10 ? '0' : '') + h + `:${m}` + (includeSeconds ? `:${s}` : '') + (showMeridian ? meridian : '');
    }

    return (
        <div>
            <h2>{event.name}</h2>
            <b>{`${date_str} ${start} — ${end}`}</b>
            <p>{event.description}</p>
        </div>
    )
}

export default MeetingCard
