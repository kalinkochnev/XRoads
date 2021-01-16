import { Formik } from "formik";
import React from "react";
import { store } from "react-notifications-component";
import { useHistory } from "react-router-dom";
import * as Yup from "yup";
import { useStateValue } from "../../../service/State";
import { sendRequest } from "../../../service/xroads-api";
import Navbar from "../../Common/Navbar/Navbar";
import "../Edit/ClubCode.scss";





const ClubCode = () => {
    let history = useHistory();
    const [state, dispatch] = useStateValue();
    let school = state.user.school;

    const onSubmit = (values) => {
        console.log(values)
        sendRequest('check_code', { schoolId: school }, 'GET', null, {code: values.code}).then(response => {
            if (response.ok) {
                response.json().then(club => {
                    let url = `/school/${school}/clubs/${club.id}/edit/${values.code}`
                    console.log(url)
                    history.push(url)
                })
            } else {
                store.addNotification({
                    title: "Warning",
                    message: "Invalid club code given",
                    type: "warning",
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

    return (
        <div>
            <Navbar></Navbar>
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
