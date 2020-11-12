import React, { useState } from 'react';
import DynamicForm from '../../Common/Form/DynamicForm';
import * as Yup from 'yup';
import { withFormik } from 'formik';
import MeetingCard from '../Meeting/Meeting';
import { Link } from 'react-router-dom';


const Meetings = ({clubData}) => {
    let [displayAdd, setDisplay] = useState(true);

    const addEventClick = (e) => {
        setDisplay(false);
    }

    return (
        <div>
            {clubData.events.map(event => <MeetingCard event={event} editable={true}/>)}
            { displayAdd ? <button onClick={addEventClick}>Add event</button> : null}
        </div>
    );
}

export default Meetings;