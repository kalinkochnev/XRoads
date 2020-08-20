import React from "react";
import { Formik, Field, ErrorMessage, Form, useField } from "formik";
import * as Yup from "yup";
import "./AuthForm.scss";

const SignupForm = () => {
  function showOneError(formik) {
    let touched = Object.keys(formik.touched);
    for (var t_field of touched) {
      let error = formik.errors[t_field];
      if (error) {
        return <div class="error-box">{error}</div>;
      }
    }
  }

  return (
    <Formik
      initialValues={{
        email: "",
        firstName: "",
        lastName: "",
        password1: "",
        password2: "",
      }}
      validationSchema={Yup.object({
        email: Yup.string()
          .required("Email required")
          .email("Please provide a valid email"),
        firstName: Yup.string()
          .required("First name required")
          .max(15, "Must be 15 characters or less"),
        lastName: Yup.string()
          .required("Last name required")
          .max(15, "Must be 15 characters or less"),
        password1: Yup.string()
          .required("Password required")
          .min(8, "Password must be 8 characters or more"),
        password2: Yup.string()
          .required("Confirm password required")
          .min(8, "Password must be 8 characters or more")
          .test("passwords-match", "Passwords must match", function (value) {
            return this.parent.password1 == value;
          }),
      })}
      onSubmit={(values, { setSubmitting }) => {
        // TODO send request to the server
        setTimeout(() => {
          alert(JSON.stringify(values, null, 2));
          setSubmitting(false);
        }, 400);
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
                {...formik.getFieldProps("firstName")}
              />
              <input
                type="text"
                placeholder="Last name"
                {...formik.getFieldProps("lastName")}
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
              {showOneError(formik)}
            </div>
          </form>
        </div>
      )}
    </Formik>
  );
};

export default SignupForm;
{
  /* <Form className="accountForm">
          <div className="fields">
            <Field
              name="email"
              type="email"
              className="first-field"
              placeholder="Email Address"
            />
            <Field name="firstName" type="text" placeholder="First name" />
            <Field name="lastName" type="text" placeholder="Last name" />
            <Field name="password1" type="password" placeholder="Password" />
            <Field
              className="last-field"
              name="password2"
              type="password"
              placeholder="Confirm Password"
            />

            <button type="submit" id="account-submit">
              Sign up
            </button>
          </div>
        </Form>
        <ErrorMessage name="email" />
      <ErrorMessage name="firstName" />
      <ErrorMessage name="lastName" />
      <ErrorMessage name="password1" />
      <ErrorMessage name="password2" /> */
}

// class SignupForm extends React.Component {

//     render() {
//         return (
//             <div class="accountLayout">
//                 <form class="accountForm">
//                     <div class="fields">
//                         <input class="first-field" type="email" name="email-address" placeholder="Email Address" />
//                         <input type="text" name="first-name" placeholder="First name" />
//                         <input type="text" name="last-name" placeholder="Last name" />
//                         <input type="password" name="password" placeholder="Password" />
//                         <input class="last-field" type="password" name="password" placeholder="Confirm Password" />
//                     </div>
//                 </form>
//             </div>
//         );
//     }
// }
