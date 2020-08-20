import React from 'react';
import { Formik, Field, ErrorMessage, Form } from 'formik';
import * as Yup from 'yup';
import './AuthForm.scss';

const SignupForm = () => {
    return (
        <Formik
            initialValues={{ email: '', firstName: '', lastName: '', password1: '', password2: '' }}
            validationSchema={Yup.object({
                email: Yup.string().required('Required').email('Please provide a valid email'),
                firstName: Yup.string().required('Required'),
                lastName: Yup.string().required('Required')
                    .max(15, 'Must be 15 characters or less'),
                password1: Yup.string().required('Required')
                    .min(8, 'Password must be 8 characters or more'),
                password2: Yup.string().required('Required')
                    .min(8, 'Password must be 8 characters or more')
                    .test('passwords-match', 'Passwords must match', function (value) {
                        return this.parent.password1 == value
                    })
            })}
            onSubmit={(values, { setSubmitting }) => {
                // TODO send request to the server
                setTimeout(() => {
                  alert(JSON.stringify(values, null, 2));
                  setSubmitting(false);
                }, 400);
            }}
        >
            <Form>
                <Field name="email" type="email"/>
                <ErrorMessage name="email" />

                <Field name="firstName" type="text"/>
                <ErrorMessage name="firstName" />

                <Field name="lastName" type="text"/>
                <ErrorMessage name="lastName" />

                <Field name="password1" type="password"/>
                <ErrorMessage name="password1" />

                <Field name="password2" type="password"/>
                <ErrorMessage name="password2" />

            </Form>
        </Formik>
    )
}

export default SignupForm;
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
//                     <input id="account-submit" type="submit" value="sign up" />
//                 </form>
//             </div>
//         );
//     }
// }