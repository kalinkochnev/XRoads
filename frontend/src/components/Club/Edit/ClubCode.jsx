import { Formik } from "formik";
import React from "react";
import { useHistory } from "react-router-dom";
import * as Yup from "yup";
import { useStateValue } from "../../../service/State";
import { sendRequest } from "../../../service/xroads-api";
import Navbar from "../../Common/Navbar/Navbar";
import "../Edit/ClubCode.scss";
import 'react-notifications/lib/notifications.css';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import { useContext } from "react";
import { ClubContext } from "../../../screens/Club/Routes";
import { Cookies } from "react-cookie";

const ClubCode = () => {
    let history = useHistory();
    const [state, dispatch] = useStateValue();
    let school = state.user.school;
    const [club, setClub] = useContext(ClubContext);

    const onSubmit = (values) => {
        sendRequest('check_code', { schoolSlug: school }, 'GET', null, {code: values.code}).then(response => {
            if (response.ok) {
                response.json().then(club => {
                    setClub({...club, code: values.code})
                    new Cookies().set("club_code", values.code)
                    let url = `/${school}/${club.slug}/edit/`
                    history.push(url)
                })
            } else {
                NotificationManager.error("Not a valid club code", "Failure")
            }

        })
    }

    return (
        <div>
            <Navbar></Navbar>
            <NotificationContainer />
            <div className="center-form">
                <Formik
                    initialValues={{ code: '' }}
                    validationSchema={Yup.object({
                        code: Yup.string().required()
                    })}
                    onSubmit={onSubmit}
                >
                    {(formik) => (
                        <form className="xr-form" onSubmit={formik.handleSubmit}>

                            <div className="fields">
                                <label><h2>Enter your club code</h2></label>
                                <input id="only-field" placeholder="Club code" {...formik.getFieldProps("code")}></input>
                                <button id="xr-submit" type="submit">Edit now!</button>
                            </div>
                        </form>
                    )}
                </Formik>
            </div>

        </div>
    );
};

export default ClubCode;
