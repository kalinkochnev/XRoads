import React, { useContext, useState } from "react";
import DynamicForm from '../../Common/Form/DynamicForm';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import moment from "moment";
import { sendRequest } from "../../../service/xroads-api";
import { ClubContext } from "../../../screens/Club/Routes";
import { store } from "react-notifications-component";
import "react-confirm-alert/src/react-confirm-alert.css"; // Import css for alert
import Dayz from "dayz";

const MeetingsEdit = () => {
    const [club, setClub] = useContext(ClubContext);
    let [displayAdd, setDisplay] = useState(true);
    let [events, setEvents] = [club.events, (events) => setClub({ ...club, events: events })];

    const addEventClick = (e) => {
        setDisplay(!displayAdd);
    }

    return (
        <div>
            {events.map(event => <MeetingCard event={event} editable={true} state={[events, setEvents]} />)}
            { displayAdd ? <button onClick={addEventClick}>Add event</button> : <MeetingCard event={{}} displayEdit={true} editable={true} setDisplay={setDisplay} />}
        </div>
    );
}

const MeetingFormFunc = (initialData = {}, setDisplay = (bool) => null) => {
    const fieldData = {
        name: {
            initialValue: "",
            type: 'text',
            fieldProps: {
                label: 'Meeting name'
            },
            validation: Yup.string().required(),
        },
        date: {
            initialValue: moment().format("yyyy-MM-DD"),
            type: 'date-selector',
            fieldProps: {
                label: 'Meeting Date'
            },
            validation: Yup.date().required()
        },
        start: {
            initialValue: moment("14:15:00", 'H:mm:ss').toDate(),
            type: 'time-selector',
            fieldProps: {
                label: 'Start time'
            },
            validation: Yup.date().required()
        },
        end: {
            initialValue: moment("15:15:00", 'H:mm:ss').toDate(),
            type: 'time-selector',
            fieldProps: {
                label: 'End time'
            },
            validation: Yup.date().min(Yup.ref('start'), "End time must be sometime after start time")
        },
        description: {
            type: 'text',
            initialValue: 'Some initial value',
            fieldProps: {
                label: 'Meeting description'
            },
            validation: Yup.string().required(),
        },
    }
    const [club, setClub] = useContext(ClubContext);
    let [events, setEvents] = [club.events, (events) => setClub({ ...club, events: events })];
    const [fieldsJSX, getInitialValues, getValidation] = DynamicForm(fieldData, initialData);
    const Form = (formik) => (
        <form className="editBody" onSubmit={formik.handleSubmit}>
            {fieldsJSX(formik)}
            <button type="submit" id="club-submit" disabled={formik.isSubmitting}>{Object.keys(initialData).length == 0 ? "Create Event" : "Save Event"}</button>
            <button type="reset" id="club-reset" onClick={() => handleReset(formik)}>Cancel Event</button>
        </form>
    )

    const updateEvent = (values, club, initialData) => {
        // Send PUT request to server to update event
        let eventId = initialData.id
        let urlParams = { clubId: club.id, clubCode: club.code, eventId: eventId}
        sendRequest('event', urlParams, "PUT", values).then(response => {
            if (response.ok) {
                response.json().then(body => {
                    // Update the club event state
                    let newEvents = events.map(event => {
                        if (event.id == initialData.id) {
                            event = body
                        }
                        return event
                    })
                    setEvents(newEvents); 
                })
                store.addNotification({
                    title: "Event updated!",
                    message: "Event " + values.name + " has been saved!",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    dismiss: {
                        duration: 5000,
                        onScreen: true,
                    },
                });
            }

        })
    }

    const createEvent = (values, club, initialData) => {
        let urlParams = { clubId: club.id, clubCode: club.code }
        sendRequest('event_create', urlParams, "POST", values).then(response => {
            if (response.ok) {
                // Create the new event and update state
                response.json().then(body => {
                    setEvents([...events, body]);
                })
                store.addNotification({
                    title: "Event Created!",
                    message: "Event " + values.name + " has been created!",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    dismiss: {
                        duration: 5000,
                        onScreen: true,
                    },
                });
            }
            
        })
    }

    const cancelEvent = () => {
        let eventId = initialData.id
        let urlParams = { clubId: club.id, clubCode: club.code, eventId: eventId}
        sendRequest('event', urlParams, "DELETE", {}).then(response => {
            if (response.ok) {
                // Create the new event and update state
                response.json().then(body => {
                    setEvents(events.map(event => event.id != eventId));
                })
                store.addNotification({
                    title: "Event Cancelled",
                    message: "Event was successfully canceled",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    dismiss: {
                        duration: 5000,
                        onScreen: true,
                    },
                });
            }

        })
    }

    const saveInfo = (values, { setSubmitting }) => {
        const formatTime = (time) => moment(time).format("H:mm:ss")
        const formatDate = (date) => moment(date).format("yyyy-MM-DD")
        values = { ...values, start: formatTime(values.start), end: formatTime(values.end), date: formatDate(values.date) }

        if (Object.keys(initialData).includes("id")) {
            updateEvent(values, club, initialData)
        } else {
            createEvent(values, club, initialData)
        }
        setSubmitting(false);
    }

    const handleReset = (formik) => {
        if (window.confirm("Are you sure you want to cancel the event?")) {
            if (Object.keys(initialData).length != 0) {
                // Remove the event from the events being displayed
                setEvents(events.filter(event => event.id != initialData.id));
                cancelEvent()
            } else {
                setDisplay(true);
            }
            formik.resetForm()
        }
    }

    const formikEnhancer = withFormik({
        mapPropsToValues: props => getInitialValues(),
        validationSchema: Yup.object().shape(getValidation()),
        handleSubmit: saveInfo,
        displayName: 'Edit Meeting',
    });

    return formikEnhancer(Form);
}

const MeetingCard = ({ event, editable = false, displayEdit = false, state = {}, setDisplay = null }) => {
    let [showEdit, setEdit] = useState(displayEdit);
    const MeetingForm = MeetingFormFunc(event, state, setDisplay)

    if (Object.keys(event).length == 0) {
        return showEdit ? <MeetingForm /> : null;
    }

    let date_str = new Date(event.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'utc' });
    let start = moment(event.start, 'H:mm:ss').format('h:mm a');
    let end = moment(event.end, 'H:mm:ss').format('h:mm a');
    const handleClick = (e) => {
        if (editable) {
            setEdit(!showEdit);
        }
    }

    return (
        <div>
            <h2>{event.name}</h2>
            <b>{`${date_str}  ${start} — ${end}`}</b>
            {editable ? <button onClick={handleClick}>Edit</button> : null}
            <p>{event.description}</p>
            <br />
            {showEdit ? <MeetingForm /> : null}
        </div>
    )
}

const CalendarView = ({events}) => {
    let dayzEvents = Dayz.EventsCollection(events.map(event => {return {content: event.name, range: moment}}))

    return (
      <div>
        <Dayz display="month" date={props.date} events={EVENTS} />
      </div>
    );
};


export { MeetingsEdit, MeetingCard };
