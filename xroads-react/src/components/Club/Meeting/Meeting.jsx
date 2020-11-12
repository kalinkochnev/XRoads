import React, { useState } from "react";
import DynamicForm from '../../Common/Form/DynamicForm';
import * as Yup from 'yup';
import { withFormik } from 'formik';



const MeetingForm = ({initialData={}}) => {
    const fieldData = {
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
            {console.log(fieldsJSX(formik))}
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

const MeetingCard = ({ event, editable=false }) => {
    let [showEdit, setEdit] = useState(editable);
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

    const handleClick = (e) => {
        if (editable) {
            setEdit(true);
        }
    }

    const MeetingSDds = MeetingForm({})

    return (
        <div>
            <h2>{event.name}</h2>
            <button onClick={handleClick}>Edit</button>
            <b>{`${date_str} ${start} — ${end}`}</b>
            <p>{event.description}</p>
            <br />
            <MeetingSDds initialData={event}></MeetingSDds>
        </div>
    )
}



export default MeetingCard
