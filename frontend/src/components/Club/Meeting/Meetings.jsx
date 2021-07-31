import React, { useContext, useState } from "react";
import DynamicForm from '../../Common/Form/DynamicForm';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import moment from "moment";
import { sendRequest } from "../../../service/xroads-api";
import { ClubContext } from "../../../screens/Club/Routes";
import "./Meetings.scss";
import 'react-notifications/lib/notifications.css';
import { NotificationContainer, NotificationManager } from 'react-notifications';

const MeetingsEdit = () => {
    const [club, setClub] = useContext(ClubContext);
    let [displayAdd, setDisplay] = useState(true);
    let [events, setEvents] = [club.events, (events) => setClub({ ...club, events: events })];

    const addEventClick = (e) => {
        setDisplay(!displayAdd);
    }

    return (
        <div>
            <NotificationContainer />
            {events.map(event => <MeetingCard event={event} editable={true} state={[events, setEvents]} />)}
            {displayAdd ? <button className="defaultButton" onClick={addEventClick}>Add event</button> : <MeetingCard event={{}} displayEdit={true} editable={true} setDisplay={setDisplay} />}
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

            <div className="date-start-end">
                {fieldsJSX(formik, ['date', 'start', 'end'])}
            </div>
            {fieldsJSX(formik, ['name', 'description'])}
            {Object.keys(initialData).length == 0 ?
                <button type="submit" id="club-submit" className="defaultButton" onClick={() => createEvent(formik.values, club)} disabled={formik.isSubmitting}>Create Event</button>

                :
                <button type="submit" className="defaultButton" id="club-submit" onClick={() => updateEvent(formik.values, club, initialData)} disabled={formik.isSubmitting}>Save Event</button>

            }
            <button type="reset" className="defaultButton outline" id="club-reset" onClick={() => handleReset(formik)}>Cancel Event</button>
        </form>
    )

    const updateEvent = (values, club, initialData) => {
        // Send PUT request to server to update event
        let eventId = initialData.id
        let urlParams = { clubSlug: club.slug, clubCode: club.code, eventId: eventId }
        sendRequest('event_edit', urlParams, "PATCH", values).then(response => {
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
                // store.addNotification({
                //     title: "Event updated!",
                //     message: "Event " + values.name + " has been saved!",
                //     type: "success",
                //     insert: "top",
                //     container: "top-right",
                //     dismiss: {
                //         duration: 5000,
                //         onScreen: true,
                //     },
                // });
                NotificationManager.success("Event updated successfully", "Event updated")
            }

        })
    }

    const createEvent = (values, club) => {
        // console.log(values)
        let urlParams = { clubSlug: club.slug, clubCode: club.code }
        sendRequest('event_create', urlParams, "POST", values).then(response => {
            if (response.ok) {
                // Create the new event and update state
                response.json().then(body => {
                    // console.log(body);
                    setEvents([...events, body]);
                })
                // store.addNotification({
                //     title: "Event Created!",
                //     message: "Event " + values.name + " has been created!",
                //     type: "success",
                //     insert: "top",
                //     container: "top-right",
                //     dismiss: {
                //         duration: 5000,
                //         onScreen: true,
                //     },
                // });
                NotificationManager.success("Event created successfully", "Event created")
            }

        })
    }

    const cancelEvent = () => {
        let eventId = initialData.id
        let urlParams = { clubSlug: club.slug, clubCode: club.code, eventId: eventId }
        sendRequest('event_edit', urlParams, "DELETE", {}).then(response => {
            if (response.ok) {
                // Create the new event and update state
                response.json().then(body => {
                    setEvents(events.map(event => event.id != eventId));
                })
                // store.addNotification({
                //     title: "Event Cancelled",
                //     message: "Event was successfully canceled",
                //     type: "success",
                //     insert: "top",
                //     container: "top-right",
                //     dismiss: {
                //         duration: 5000,
                //         onScreen: true,
                //     },
                // });
                NotificationManager.info("Event cancelled successfully", "Event cancelled")
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
        if (Object.keys(initialData).length != 0) {
            // Remove the event from the events being displayed
            setEvents(events.filter(event => event.id != initialData.id));
            cancelEvent()
        } else {
            setDisplay(true);
        }
        formik.resetForm()
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
        <div className="meeting-card">
            <div className="meet-basics">
                <h2>{event.name}</h2>
                {editable ? <button className="meeting-edit defaultButton" onClick={handleClick}>Edit</button> : null}
                <br />
                <b>{`${date_str}  ${start} — ${end}`}</b>

            </div>
            <div className="meet-details">
                <p>{event.description}</p>
                <br />
            </div>
            {showEdit ? <MeetingForm /> : null}
        </div>
    )
}


export { MeetingsEdit, MeetingCard };
