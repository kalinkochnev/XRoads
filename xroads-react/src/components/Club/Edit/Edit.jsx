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
import "../../Common/Form/FormStyle.scss";


const InputField = ({ label, type, ...props }) => {
    // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
    // which we can spread on <input> and also replace ErrorMessage entirely.
    const [field, meta] = useField(props);
    return (
        <>
            <label htmlFor={props.id || props.name}>{label}</label>
            { type == "textarea" ? <textarea style={{height: "200px"}} cols="2" {...field} {...props}></textarea> : <input className="text-input" {...field} {...props} />}
            {meta.touched && meta.error ? (
                <div className="error">{meta.error}</div>
            ) : null}
        </>
    );
};



const possData = ['label', 'type', 'validation', 'component']
const componentArgs = ['label', 'type']
const fieldData = {
    presentation_url: {
        label: 'Presentation Link',
        type: 'text',
        validation: Yup.string().url().matches("^.*docs\.google\.com\/presentation\/d\/(?<id>[^\/]*).*", "Please enter a valid google slides url"),
    },
    contact: {
        label: 'Club contact',
        type: 'text',
        validation: Yup.string().email("Please enter a valid contact email")
    },
    extra_info: {
        label: 'Detailed Info Email Body',
        type: 'textarea',
        validation: Yup.string(),
    },
    description: {
        label: 'Club Description',
        type: 'rich-text',
        validation: null,
        component: (formik) => (
            <div>
                <label >Club Description</label>
                <RichEditor fieldName="description" mdContent={formik.values.description} onChange={formik.handleChange} setFieldValue={formik.setFieldValue} onBlur={formik.handleBlur} />
            </div>
        ),
    },
}

// Created by following this example: https://codesandbox.io/s/QW1rqjBLl?file=/index.js:860-992
const GeneralEdit = (props) => {
    const [state, dispatch] = useStateValue();
    const [isVisible, setVisibility] = useState(props.clubData.is_visible);
    const [clubData, setClubData] = useState(props.clubData);
    

    // This returns a dictionary of every field and the associated value of that (ex want to know every fields input type)
    const filterObjByAttr = (attr, obj, fields=[], removeNull=false, emptyFieldFiller=null) => {
        let keys = fields.length == 0 ? Object.keys(obj) : fields

        let newObj = {};
        for (let key of keys) {
            if (!Object.keys(obj[key]).includes(attr)) {
                obj[key][attr] = emptyFieldFiller;
            }
            if (obj[key][attr] == null && removeNull) {
                continue
            }
            newObj[key] = obj[key][attr];
        }
        return newObj;
    }

    const objFromKeys = (keys, obj) => {
        let values = {};
        for (var field of keys) {
            values[field] = obj[field]
        }
        return values;
    }

    let getEditableFields = (() => {
        if (clubData == null) {
            return []
        }
        let fields = Object.keys(fieldData);
        if (!clubData.school.club_contact) {
            fields.pop('contact')
        }
        return fields
    });

    const getInitialValues = () => {
        return objFromKeys(getEditableFields(), clubData);
    }

    const getValidation = () => {
        return filterObjByAttr('validation', fieldData, getEditableFields(), true)
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
        let compsToRender = [];
        let compData = filterObjByAttr('component', fieldData, getEditableFields(), false, null)
        for (let key of Object.keys(compData)) {
            if (Object.keys(fieldData[key]).includes("component")) {
                if (fieldData[key].component != null) {
                    compsToRender.push(fieldData[key].component(formik))
                    continue;
                }
                
            }
            switch (fieldData[key].type){
                case "textarea":
                case "text":
                    compsToRender.push(<InputField name={key} {...objFromKeys(componentArgs, fieldData[key])}></InputField>)
                    break;
                case "rich-text":
                    compsToRender.push(fieldData[key].component(formik))
                    break;
            }
        }

        return compsToRender.map(item => item)
    }

    const Form = (formik) => (
        <form className="editBody" onSubmit={formik.handleSubmit}>
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