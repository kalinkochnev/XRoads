import React from "react";
import Dayz from "dayz";
// could also import the sass if you have a loader at dayz/dayz.scss
import "dayz/dist/dayz.css";
import moment from "moment";
let date = moment();
// would come from a network request in a "real" app
const EVENTS = new Dayz.EventsCollection([
  {
    content: "A short event",
    range: moment.range(date.clone(), date.clone().add(1, "day")),
  },
  {
    content: "Two Hours ~ 8-10",
    range: moment.range(date.clone().hour(8), date.clone().hour(10)),
  },
  {
    content: "A Longer Event",
    range: moment.range(
      date.clone().subtract(2, "days"),
      date.clone().add(8, "days")
    ),
  },
]);



export default CalendarView;
