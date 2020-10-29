import React, { useEffect } from "react";

import "./Edit.scss";

import RichEditor from "../../Common/RichEditor/RichEditor";

import { useState } from "react";
import { sendRequest, updateClub } from "../../../service/xroads-api";
import { useStateValue } from "../../../service/State";
import ReactTooltip from "react-tooltip";

import { store } from "react-notifications-component";

import "react-confirm-alert/src/react-confirm-alert.css"; // Import css for alert
import { Formik, yupToFormErrors } from "formik";
import * as Yup from 'yup';


const GeneralEdit = (props) => {
  const [state, dispatch] = useStateValue();
  const [isVisible, setVisibility] = useState(props.club.is_visible);
  const [clubData, setClubData] = useState(props.clubData);

  const TextInput = ({label, ...props}) => {
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
  }

  const TextField = ({label, ...props}) => {
    
  }

  const getFormFields = () => {

  }

  const getValues = () => {

    let possFields = {
      description: Yup.string(), 
      presentation_url: Yup.string().url().matches("^.*docs\.google\.com\/presentation\/d\/(?<id>[^\/]*).*", message="Please enter a valid google slides url"),
      hidden_info: Yup.string(),
      contact:Yup.string().email()
    }

    if (!clubData.school.club_contact) {
      delete possFields.contact
    }

    // Gets the initial values from the data that was loaded in based on what fields are given
    let initialValues = {}
    for (let key in Object.keys(possFields)) {
      initialValues[key] = possFields[key];
    }

    return {
      validation: possFields,
      initialValues: initialValues
    }
  }

  const saveClubDetails = (values, {setSubmitting}) => {
    setSubmitting(false);
    const updatedClub = {
      ...props.club,
      ...values
    };

    console.log("Updated club would be", updatedClub);
    updateClub(props.club.id, updatedClub, props.code).then(
      (res) => {
        res.json().then((updatedClub) => {
          console.log("Updated club", updateClub);
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
    );
  };

  const toggleHide = () => {
    let user = state.user;
    let urlArgs = {
      clubId: props.club.id,
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

  return (
    <div className="centerContent">
      <div className="editBody">

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

          <label class="switch">
            <input type="checkbox" onClick={toggleHide} checked={!isVisible} />
            <span className="slider round"></span>
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
      </div>
    </div>
  );
};


export { GeneralEdit };
