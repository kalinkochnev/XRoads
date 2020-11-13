import React, { useState } from "react";
import DynamicForm from '../../Common/Form/DynamicForm';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import moment from "moment";

const MeetingsEdit = ({ clubData }) => {
    let [displayAdd, setDisplay] = useState(true);

    const addEventClick = (e) => {
        setDisplay(!displayAdd);
    }
    console.log()
    return (
        <div>
            {clubData.events.map(event => <MeetingCard event={event} editable={true} />)}
            <MeetingCard event={{}} editable={true} />
            {!displayAdd ? <MeetingCard event={{}} displayEdit={true} editable={true} /> : null}
            { displayAdd ? <button onClick={addEventClick}>Add event</button> : <MeetingCard event={{}} />}
        </div>
    );
}

const MeetingFormFunc = (initialData = {}) => {
    const fieldData = {
        name: {
            initialValue: "",
            type: 'text',
            fieldProps: {
                label: 'Meeting name'
            },
            validation: Yup.string(),
        },
        date: {
            initialValue: moment().format("yyyy-MM-DD"),
            type: 'date-selector',
            fieldProps: {
                label: 'Meeting Date'
            }
        },
        start: {
            initialValue: "14:15:00",
            type: 'time-selector',
            fieldProps: {
                label: 'Start time'
            }
        },
        end: {
            initialValue: "15:15:00",
            type: 'time-selector',
            fieldProps: {
                label: 'End time'
            }
        },
        description: {
            type: 'text',
            initialValue: 'Some initial value',
            fieldProps: {
                label: 'Meeting description'
            },
            validation: Yup.string(),
        },
    }

    const [fieldsJSX, getInitialValues, getValidation] = DynamicForm(fieldData, initialData);
    console.log(getInitialValues())
    const Form = (formik) => (
        <form className="editBody" onSubmit={formik.handleSubmit}>
            {fieldsJSX(formik)}
            <button type="submit" id="club-submit" disabled={formik.isSubmitting}>Save</button>
        </form>
    )

    const saveInfo = (values, { setSubmitting }) => {

    }

    const formikEnhancer = withFormik({
        mapPropsToValues: props => getInitialValues(),
        validationSchema: Yup.object().shape(getValidation()),
        handleSubmit: saveInfo,
        displayName: 'Add Meeting'
    });

    return formikEnhancer(Form);
}

const MeetingCard = ({ event, editable = false, displayEdit = false}) => {
    let [showEdit, setEdit] = useState(displayEdit);
    const MeetingForm = MeetingFormFunc(event)

    if (Object.keys(event).length == 0) {
        return showEdit ? <MeetingForm/> : null;
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
            {editable ? <button onClick={handleClick}>Edit</button> : null}

            <b>{`${date_str}  ${start} — ${end}`}</b>
            <p>{event.description}</p>
            <br />
            {showEdit ? <MeetingForm initialData={event} /> : null}

        </div>
    )
}



export { MeetingsEdit, MeetingCard };
