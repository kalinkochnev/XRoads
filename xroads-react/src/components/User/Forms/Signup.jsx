import React from "react";
import { Formik } from "formik";
import * as Yup from "yup";
import "./AuthForm.scss";
import { signup } from "../../../service/xroads-api";
import {showOneError, defaultFail, displayFormHelp} from "./helper"

const SignupForm = ({ setAlert }) => {

  return (
    <Formik
      initialValues={{
        email: "",
        first_name: "",
        last_name: "",
        password1: "",
        password2: "",
      }}
      validationSchema={Yup.object({
        email: Yup.string()
          .required("Email required")
          .email("Please provide a valid email"),
        first_name: Yup.string()
          .required("First name required")
          .max(15, "Must be 15 characters or less"),
        last_name: Yup.string()
          .required("Last name required")
          .max(15, "Must be 15 characters or less"),
        password1: Yup.string()
          .required("Password required")
          .min(8, "Password must be 8 characters or more"),
        password2: Yup.string()
          .required("Confirm password required")
          .min(8, "Password must be 8 characters or more")
          .test("passwords-match", "Passwords must match", function (value) {
            return this.parent.password1 === value;
          }),
      })}
      onSubmit={async (values, { setSubmitting, setFieldError }) => {
        // TODO send request to the server
        let response = await signup(values);
        function successCallback(response, functions, data) {
          functions.setAlert("success", "You signed up successfully! Please check your email for confirmation", false);
        }

        let funcs = {
          'setAlert': setAlert, 'setSubmitting': setSubmitting, 'setFieldError': setFieldError
        }
        displayFormHelp(response, { 'values': values }, funcs, successCallback, defaultFail)


        setSubmitting(false);
      }}
    >
      {(formik) => (
        <div class="accountLayout">
          <form onSubmit={formik.handleSubmit} className="accountForm">
            <div class="fields">
              <input
                class="first-field"
                type="email"
                placeholder="Email address"
                {...formik.getFieldProps("email")}
              />

              <input
                type="text"
                placeholder="First name"
                {...formik.getFieldProps("first_name")}
              />
              <input
                type="text"
                placeholder="Last name"
                {...formik.getFieldProps("last_name")}
              />
              <input
                type="password"
                placeholder="Password"
                {...formik.getFieldProps("password1")}
              />
              <input
                class="last-field"
                type="password"
                placeholder="Confirm Password"
                {...formik.getFieldProps("password2")}
              />

              <button type="submit" id="account-submit">
                Sign up
              </button>
            </div>
            {showOneError(formik)}
          </form>
        </div>
      )}

    </Formik>
  );
};

export default SignupForm;
