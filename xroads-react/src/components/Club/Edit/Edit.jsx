import React, { useContext, useEffect } from "react";

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
import "../../Common/Form/FormStyle.scss";
import DynamicForm from "../../Common/Form/DynamicForm";
import { ClubContext } from "../../../screens/Club/Routes";

const fieldData = {
    presentation_url: {
        type: 'text',
        fieldProps: {
            label: 'Presentation Link',
        },
        validation: Yup.string().url().matches("^.*docs\.google\.com\/presentation\/d\/(?<id>[^\/]*).*", "Please enter a valid google slides url"),
    },
    contact: {
        type: 'text',
        fieldProps: {
            label: 'Club contact',
        },
        validation: Yup.string().email("Please enter a valid contact email")
    },
    extra_info: {
        type: 'textarea',
        fieldProps: {
            label: 'Detailed Info Email Body',
        },
        validation: Yup.string(),
    },
    description: {
        fieldProps: {
            label: 'Club Page Description'
        },
        type: 'rich-text',
    },
}

// Created by following this example: https://codesandbox.io/s/QW1rqjBLl?file=/index.js:860-992
const GeneralEdit = (props) => {
    const [state, dispatch] = useStateValue();
    const [club, setClub] = useContext(ClubContext);
    const [isVisible, setVisibility] = useState(club.is_visible);

    // This returns a dictionary of every field and the associated value of that (ex want to know every fields input type)
    const saveClubInfo = (values, { setSubmitting }) => {
        updateClub(club.id, values, club.code).then((res) => {
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

    const getEditableFields = (fields, data) => {
        if (data == null) {
            return []
        }
        if (!data.school.club_contact) {
            fields.splice(fields.indexOf('contact'), 1)
        }
        console.log(fields);
        return fields;
    }
    

    const [fieldsJSX, getInitialValues, getValidation] = DynamicForm(fieldData, club, getEditableFields);

    const Form = (formik) => (
        <form className="editBody" onSubmit={formik.handleSubmit}>
            {fieldsJSX(formik)}
            <button type="submit" id="club-submit" disabled={formik.isSubmitting}>Save</button>
        </form>
    )

    const formikEnhancer = withFormik({
        mapPropsToValues: props => getInitialValues(),
        validationSchema: Yup.object().shape(getValidation()),
        handleSubmit: saveClubInfo,
        displayName: 'Main Editor'
    });

    const toggleHide = () => {
        let user = state.user;
        let urlArgs = {
            clubId: club.id,
            code: club.code
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