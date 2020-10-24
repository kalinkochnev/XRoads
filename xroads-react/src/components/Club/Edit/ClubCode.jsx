import "../Edit/ClubCode.scss";

import { Formik } from "formik";
import * as Yup from "yup";

import React from "react";
import Navbar from "../../Common/Navbar/Navbar";

const ClubCode = (props) => {
    return (
        <div>
            <Navbar></Navbar>
            <div className="center-form">
            <Formik
                initialValues={{ code: '' }}
                validationSchema={Yup.object({
                    code: Yup.string().required()
                })}
            >
                {(formik) => (
                    <form className="xr-form" onSubmit={formik.handleSubmit}>

                        <div className="fields">
                            <label><h2>Enter your club code</h2></label>
                            <input id="only-field" placeholder="Club code"></input>
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
