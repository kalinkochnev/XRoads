import React from "react";
import { Formik } from "formik";
import * as Yup from "yup";
import "./AuthForm.scss";
import { login } from "../../../service/xroads-api";
import { useCookies } from "react-cookie";
import { useHistory } from 'react-router-dom';
import {displayFormHelp, defaultFail} from '../../../components/User/Forms/helper';


const LoginForm = ({ setAlert })  => {

  let history = useHistory();

  // const [cookies, setCookie] = useCookies(['xroads-jwt-token']);

  function showOneError(formik) {
    let touched = Object.keys(formik.touched);
    for (var t_field of touched) {
      let error = formik.errors[t_field];
      if (error) {
        return <div className="error-box">{error}</div>;
      }
    }
  }

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

        let successCallback = (response, functions, data) => {
          functions.setAlert("success", "You logged in successfully!", true);
          // response.json().then( jwt => {
          //   console.log("received token ", jwt);
          //   setCookie("xroads-token", jwt, { path: "/"});
          //   console.log("Redirecting to clubs");
          //   history.push('/clubs');
          // });
        }

        let funcs = {
          'setAlert': setAlert
        }

        displayFormHelp(response, { 'values': values }, funcs, successCallback, defaultFail)

        setSubmitting(false);
      }}
    >
      {(formik) => (
        <div className="accountLayout">
          <form onSubmit={formik.handleSubmit} className="accountForm">
            <div className="fields">
              <input
                className="first-field"
                type="email"
                placeholder="Email address"
                {...formik.getFieldProps("email")}
              />

              <input
                className="last-field"
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
