import React, { useEffect } from "react";

import "./Edit.scss";

import RichEditor from "../../Common/RichEditor/RichEditor";

import { useState } from "react";
import { sendRequest, updateClub } from "../../../service/xroads-api";
import { useStateValue } from "../../../service/State";
import ReactTooltip from "react-tooltip";

import { store } from "react-notifications-component";

import "react-confirm-alert/src/react-confirm-alert.css"; // Import css for alert
import { Formik, useField, withFormik, yupToFormErrors } from "formik";
import * as Yup from 'yup';
import { ContentState, EditorState } from "draft-js";


const InputField = ({ label, ...props }) => {
    // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
    // which we can spread on <input> and also replace ErrorMessage entirely.
    const [field, meta] = useField(props);
    return (
        <>
            <label htmlFor={props.id || props.name}>{label}</label>
            <input className="text-input" {...field} {...props} />
            {meta.touched && meta.error ? (
                <div className="error">{meta.error}</div>
            ) : null}
        </>
    );
};

// Created by following this example: https://codesandbox.io/s/QW1rqjBLl?file=/index.js:860-992
const GeneralEdit = (props) => {
    const [state, dispatch] = useStateValue();
    const [isVisible, setVisibility] = useState(props.clubData.is_visible);
    const [clubData, setClubData] = useState(props.clubData);

    let editableFields = (() => {
        if (clubData == null) {
            return []
        }
        let fields = ['presentation_url', 'hidden_info', 'description']

        if (clubData.school.club_contact) {
            fields.push('contact')
        }

        return fields
    })();

    const objFromKeys = (keys, obj) => {
        let values = {};
        for (var field of keys) {
            values[field] = obj[field]
        }
        return values;
    }

    const getInitialValues = () => {
        console.log(clubData)
        return objFromKeys(editableFields, clubData);
    }

    const getValidation = () => {
        let possFields = {
            description: Yup.string(),
            presentation_url: Yup.string().url().matches("^.*docs\.google\.com\/presentation\/d\/(?<id>[^\/]*).*", "Please enter a valid google slides url"),
            hidden_info: Yup.string(),
            contact: Yup.string().email()
        }
        return objFromKeys(editableFields, possFields)
    }

    const saveClubInfo = (values, { setSubmitting }) => {
        updateClub(clubData.id, values, props.code).then((res) => {
            if (res.ok) {
                res.json().then(() => {
                    store.addNotification({
                        title: "Saved",
                        message: "Club details successfully saved",
                        type: "success",
                        insert: "top",
                        container: "top-right",
                        dismiss: {
                            duration: 5000,
                            onScreen: true,
                        },
                    });
                });
            }
            
        }
        );
        setSubmitting(false);
    };

    const formikEnhancer = withFormik({
        mapPropsToValues: props => getInitialValues(),
        validationSchema: Yup.object().shape(getValidation()),
        handleSubmit: saveClubInfo,
        displayName: 'Main Editor'
    });

    // This is where you should define individual field's JSX. This will then render the propers fields into the form
    const fieldsJSX = (formik) => {
        let fieldJSX = {
            description: (
                <div>
                    <label>Club Description</label>
                    <RichEditor fieldName="description" mdContent={formik.values.description} onChange={formik.handleChange} setFieldValue={formik.setFieldValue} onBlur={formik.handleBlur} />
                </div>
            ),
            presentation_url: (<InputField label="Presentation URL" name="presentation_url" type="text"></InputField>),
            hidden_info: (<InputField label="Detailed info email body" name="hidden_info" type="text"></InputField>),
            contact: (<InputField label="Club contact email" name="contact" type="text"></InputField>)
        }

        let jsxToRender = [];
        for (let field of editableFields) {
            jsxToRender.push(fieldJSX[field]);
        }

        return jsxToRender.map(item => item)
    }

    const Form = (formik) => (
        <form onSubmit={formik.handleSubmit}>
            {fieldsJSX(formik)}
            <button type="submit" id="club-submit" disabled={formik.isSubmitting}>Save</button>
        </form>
    )

    const toggleHide = () => {
        let user = state.user;
        let urlArgs = {
            clubId: clubData.id,
            code: props.code
        };
        sendRequest("toggle_hide_club", urlArgs, "POST", {}).then((response) => {
            if (response.ok) {
                setVisibility(!isVisible);
                console.log("The club is now " + isVisible.toString());
                store.addNotification({
                    title: "Club " + (isVisible ? "Hidden" : "Visible"),
                    message:
                        "The club is now visible to " +
                        (isVisible ? "club editors only" : "all users"),
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    dismiss: {
                        duration: 5000,
                        onScreen: true,
                    },
                });
            }
        });
    };

    const EditForm = formikEnhancer(Form);

    return (
        <div className="centerContent">
            <div className="editBody">
                <label>Hide club</label>
                <label className="switch">
                    <input type="checkbox" onClick={toggleHide} checked={!isVisible} />
                    <span className="slider round"></span>
                </label>
                <EditForm></EditForm>
            </div>
        </div>
    );
};


export { GeneralEdit };

/*
<Formik
          initialValues={getValues().initialValues}
          validationSchema={Yup.object(getValues().validation)}
          onSubmit={saveClubDetails}
        >

        <label htmlFor="firstName">First Name</label>
         <Field name="firstName" type="text" />
         <ErrorMessage name="firstName" />

        </Formik>
        <form className="clubEdit">
          <label className="" htmlFor="">
            Hide club
          </label>


          <ReactTooltip place="right" effect="solid" />

          <label className="" htmlFor="description">
            Description
            <br />
            <RichEditor
              mdContent={clubDescriptionMd}
              onChange={handleClubDescription}
            />
            <br />

          </label>

          <label className="" htmlFor="presentation url">
            Google Slides Link
            <br />
            <input
              type="text"
              id="presentation url"
              name="presentation url"
              value={clubJoinPromo}
              onChange={(e) => setClubJoinPromo(e.target.value)}
            />
          </label>
          <ReactTooltip place="right" effect="solid" />

        </form>
        <button type="submit" id="club-submit" onClick={saveClubDetails}>
          Save
        </button>
*/