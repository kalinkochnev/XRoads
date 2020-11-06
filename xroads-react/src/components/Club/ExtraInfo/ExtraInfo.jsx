import React, { useEffect, useState } from 'react';
import { useStateValue } from '../../../service/State';
import { sendRequest } from '../../../service/xroads-api';
import "./ExtraInfo.scss"
import { store } from "react-notifications-component";

let yup = require('yup');

const GetEmail = ({ emailCallback, closeCallback }) => {
    const [email, setEmail] = useState('');
    const [isEnabled, setEnabled] = useState(false)

    let schema = yup.object().shape({email: yup.string().email().required()})

    const emailValid = (e) => {
        setEmail(e.target.value)

        schema.isValid({email: e.target.value}).then(value => {
            if (value) {
                setEnabled(true);
            } else {
                setEnabled(false);
            }
        })
         
    }
    return (
        <div className="popup">
            <div className="popup_inner">
                <input onChange={(e) => emailValid(e)} type="email" placeholder="Enter your email here!"></input>
                <button onClick={() => {
                    emailCallback(email)
                    closeCallback()
                }
                } type="submit" disabled={!isEnabled}>Save</button>
                <button onClick={closeCallback}>Close</button>
                { !isEnabled && (email != null && email != '') ? <p>The email you entered is invalid</p> : null}
            </div>
        </div>
    );
}

const ExtraInfo = ({club}) => {
    let [state, dispatch] = useStateValue();
    let [showPopup, setPopup] = useState(false);

    console.log(showPopup);
    const getExtraInfo = () => {
        if (state.user.email == null || state.user.email == '') {
            setPopup(true)
        } else {
            sendRequest('extra_info', {clubId: club.id}, 'GET', {}, {email: state.user.email}).then(res => {
                res.json().then(body => {
                    if (res.ok) {
                        store.addNotification({
                            title: "Extra info sent!",
                            message: "Check your email for more info about " + club.name,
                            type: "success",
                            insert: "top",
                            container: "top-right",
                            dismiss: {
                                duration: 5000,
                                onScreen: true,
                            },
                        });
                    } else if (res.status == 406) {
                        store.addNotification({
                            title: "Error",
                            message: body.message,
                            type: "danger",
                            insert: "top",
                            container: "top-right",
                            dismiss: {
                                duration: 5000,
                                onScreen: true,
                            },
                        });
                    }
                })
            })
        }
    }

    const setEmail = (email) => {
        dispatch({ type: 'set email', payload: email })
        console.log('the email was set to ' + email)
    }

    const onClose = () => {
        setPopup(false);
    }
    return (
        <div>
            <h3>Request extra info!</h3>
            { state.user.email != null && state.user.email != '' ? (
                <div>
                    <h3>Using: {state.user.email}</h3>
                    <button onClick={() => dispatch({type: 'set email', payload: ''})}>Not you?</button>
                </div>
            ) : null}
            <button onClick={() => getExtraInfo()}>Click here!</button>
            { showPopup ? <GetEmail closeCallback={onClose} emailCallback={setEmail}></GetEmail> : null}
        </div>
    );
}

export default ExtraInfo;