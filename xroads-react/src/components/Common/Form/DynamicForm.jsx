import { useField } from "formik";
import React, { useEffect, useState } from "react";
import ReactDatePicker from "react-datepicker";
import RichEditor from "../RichEditor/RichEditor";
import "react-datepicker/dist/react-datepicker.css";
import moment from "moment";

const InputField = ({ label, type, ...props }) => {
    // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
    // which we can spread on <input> and also replace ErrorMessage entirely.
    const [field, meta] = useField(props);
    return (
        <>
            <label htmlFor={props.id || props.name}>{label}</label>
            { type == "textarea" ? <textarea style={{ height: "200px" }} cols="2" {...field} {...props}></textarea> : <input className="text-input" {...field} {...props} />}
            {meta.touched && meta.error ? (
                <div className="error">{meta.error}</div>
            ) : null}
        </>
    );
};

const FormikTextEditor = ({ label, name }) => {
    const [field, meta, helpers] = useField(name)
    const initial = meta.initialValue;
    const { setValue } = helpers;

    return (
        <div>
            <label>{label}</label>
            <RichEditor initialValue={initial} setValue={setValue}></RichEditor>
        </div>
    );
}

const TimePicker = ({ label, name }) => {
    const [field, meta, helpers] = useField(name);
    const value = () => moment(meta.value, 'H:mm:ss').toDate();
    const { setValue } = helpers;

    useEffect(() => {
        setValue(value())
    }, [])

    return (
        <div>
            <label>{label}</label>
            <ReactDatePicker
                selected={value()}
                onChange={date => {
                    if (moment(date).isValid()) {
                        setValue(date);
                    } else {
                        setValue(moment().toDate())
                    }
                }}
                showTimeSelect
                showTimeSelectOnly
                timeIntervals={15}
                timeCaption="Time"
                dateFormat="h:mm aa"
            />
            {meta.touched && meta.error ? (
                <div className="error">{meta.error}</div>
            ) : null}
        </div>

    );
}

const DatePicker = ({ label, name }) => {
    const [field, meta, helpers] = useField(name);
    const value = moment(meta.value, 'yyyy-MM-DD').toDate();
    const { setValue } = helpers;
    return (
        <div>
            <label>{label}</label>
            <ReactDatePicker
                selected={value}
                onChange={date => {
                    if (moment(date).isValid()) {
                        setValue(date);
                    } else {
                        setValue(moment().toDate())
                    }
                }}
                dateFormat="MM/dd/yyyy"
            />
            {meta.touched && meta.error ? (
                <div className="error">{meta.error}</div>
            ) : null}

        </div>
    );
}

const DynamicForm = (fieldData, data, editableFields = null) => {
    /* 
    attr:
        The key you want to evaluate for child elements. Ex: if attr="attr1", 
        for each key value pair in the object, it retrieves the child object's
        provided attr  {a: { attr1: 1, attr2: 2} }, in this case it returns {a: 1}
    
    obj: A JS object that has also has children as its values

    fields: This array specifies which key values to retrieve the attribute for. If
    an empty array, all fields are used.

    skipLogic: If you provide skipLogic=(key, value) => boolean, when it evaluates 
    to true, that key value pair will not be included in the result

    attrFiller:
        If the object does not have that attr in its child object,
        this calls a function that returns what value should stand in
        its place. (field, data) => filler value
    */
    const objByChildAttr = (attr, obj, fields = [], skipLogic = null, attrFiller = null) => {
        skipLogic = skipLogic == null ? (key, value) => false : skipLogic
        attrFiller = attrFiller == null ? (child, data) => null : attrFiller
        fields = fields.length == 0 ? Object.keys(obj) : fields

        let filtered = {};
        for (let field of fields) {
            // if the object does not have the attr
            if (!Object.keys(obj[field]).includes(attr)) {
                filtered[field] = attrFiller(field, data)
            }
            if (skipLogic(field, obj[field][attr])) {
                continue;
            }
            filtered[field] = obj[field][attr];
        }
        return filtered;
    }

    /* This returns an object with only the specified keys included */
    const objFromKeys = (keys, obj) => {
        let values = {};
        for (var field of keys) {
            values[field] = obj[field]
        }
        return values;
    }

    /* This retrieves the editable fields based on some conditions. 
    By default all fields are editable */
    let getEditableFields = editableFields == null ? () => Object.keys(fieldData) : () => editableFields(Object.keys(fieldData), data)
    /* This retrieves the initial values to be used in the form
    based on what fields are editable. If the provided object is empty,
    the editable fields are set to the specified default value. If
    unspecified, it will throw an exception */
    const getInitialValues = () => {
        let editableFields = getEditableFields();

        // This gets default values if it is an empty form
        if (Object.keys(data).length == 0) {
            const defaultUnspecified = (field, data) => {
                throw new Error("You did not specify initialValue for field " + field)
            }

            // This retrieves the initialValues for the fields. Throws error if unspecified. 
            return objByChildAttr('initialValue', fieldData, editableFields, null, defaultUnspecified)
        }
        return objFromKeys(editableFields, data);
    }

    /* This retrieves validation for each editable field. If validation
    is not specified, validation = null */
    const getValidation = () => {
        return objByChildAttr('validation', fieldData, getEditableFields(),)
    }

    /* Based on fieldData, this will decided which components to render for the field.
    You can specify props to be passed into the field by adding an attribute to a field
    called fieldProps. */
    const fieldsJSX = (formik, toDisplay=[]) => {
        let compsToRender = [];
        // This retrieves the components args for all the editable fields
        let compData = objByChildAttr('component', fieldData, getEditableFields(), null, null)
        // This retrieves all props to be passed into the fields of the form
        let propsFromFields = objByChildAttr('fieldProps', fieldData, getEditableFields(), null, (data, child) => { });
        
        // Specifies which fields you want to display for more customizable styling. Default all fields
        let fieldsToReturn = toDisplay.length == 0 ? Object.keys(compData) : toDisplay

        for (let field of fieldsToReturn) {
            // If a component is specified directly, it renders that instead
            if (Object.keys(fieldData[field]).includes("component")) {
                compsToRender.push(fieldData[field].component(formik))
                continue;
            }

            // If component not specified, gets proper component based on field attribute
            switch (fieldData[field].type) {
                case "textarea":
                case "text":
                    // Add props to field
                    compsToRender.push(<InputField name={field} {...propsFromFields[field]}></InputField>)
                    break;
                case "rich-text":
                    compsToRender.push(<FormikTextEditor name={field} {...propsFromFields[field]} />)
                    break;
                case "time-selector":
                    compsToRender.push(<TimePicker name={field} {...propsFromFields[field]}></TimePicker>)
                    break;
                case "date-selector":
                    compsToRender.push(<DatePicker name={field} {...propsFromFields[field]} />)
                    break;
            }
        }
        return compsToRender.map(item => item)
    }

    return [fieldsJSX, getInitialValues, getValidation]
}

export default DynamicForm;