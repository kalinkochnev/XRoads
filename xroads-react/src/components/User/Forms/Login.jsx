import React from "react";
import { Formik } from "formik";
import * as Yup from "yup";
import "./AuthForm.scss";
import { login } from "../../../service/xroads-api";
import { displayFormHelp, defaultFail, defaultOk, showOneError } from './helper';

const LoginForm = ({ setAlert }) => {
  return (
    <Formik
      initialValues={{
        email: "",
        password: "",
      }}
      validationSchema={Yup.object({
        email: Yup.string()
          .required("Email required")
          .email("Please provide a valid email"),
        password: Yup.string().required("Password required"),
      })}
      onSubmit={async (values, { setSubmitting, setFieldError }) => {
        let response = await login(values);

        function successCallback(response, functions, data) {
          functions.setAlert("success", "You logged in successfully!", false);
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
                class="last-field"
                type="password"
                placeholder="Password"
                {...formik.getFieldProps("password")}
              />

              <button type="submit" id="account-submit">
                Log in
              </button>
            </div>
            {showOneError(formik)}
          </form>
        </div>
      )}
    </Formik>
  );
};

export default LoginForm;
