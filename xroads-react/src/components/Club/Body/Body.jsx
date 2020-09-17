import React, { useEffect } from "react";
import Linkify from "react-linkify";
import { useStateValue } from "../../../service/State";
import { sendRequest } from "../../../service/xroads-api";

import { Formik } from "formik";
import * as Yup from "yup";

import "./Body.scss";
import "./../Edit/Edit.scss";
import { displayFormHelp, defaultFail } from "../../User/Forms/helper";


import { store } from 'react-notifications-component';

const Markdown = require("react-markdown");

// TODO eventually we should not have this component existing and just have it directly in the equivalent screen

const ClubBodyDetail = (props) => {
  console.log("Received club in ClubBodyDetails", props.club);

  return (
    <div className="centerContent">
      <div className="details">
        <div className="clubHeading">
          <h1>{props.club.name}</h1>

          <Linkify>
            <h2> {props.club.join_promo}</h2>
          </Linkify>
        </div>

        <Markdown source={props.club.description} />
        <AskQuestion club={props.club}></AskQuestion>

      </div>
    </div>
  );
};

const AskQuestion = (props) => {
  let club = props.club;
  const [{ user }, dispatch] = useStateValue();

  useEffect(() => {}, [user]);

  const onSubmit = (values, { setSubmitting, setFieldError }) => {    
    let urlArgs = {
      districtId: user.district,
      schoolId: user.school,
      clubId: club.id,
    };
    console.log(values)
    sendRequest("ask_question", urlArgs, "POST", values).then((response) => {
      if (response.ok) {
        store.addNotification({
          title: "Success!",
          message: "Your question was sent",
          type: "success",
          insert: "top",
          container: "top-right",
          dismiss: {
            duration: 5000,
            onScreen: true,
          },
        });
      };
    });

    setSubmitting(false);
    
  };

  return (
    <Formik
      initialValues={{ question: "" }}
      validationSchema={Yup.object({
        question: Yup.string().required("Question is required"),
      })}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <form onSubmit={formik.handleSubmit}>
            <h2> Ask a question!</h2>

            <div className="editBody" style={{marginTop: "20px"}}>
              <textarea placeholder="A very intelligent question waiting to be asked..." {...formik.getFieldProps("question")}></textarea>
            </div>
            <button type="submit" id="account-submit">
              Ask away!
            </button>
        </form>
      )}
    </Formik>
  );
};

export default ClubBodyDetail;
