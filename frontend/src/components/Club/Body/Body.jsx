import React from "react";
import Linkify from "react-linkify";
import "./../Edit/Edit.scss";
import "./Body.scss";
import Sticky from '../../Common/StickyCard/StickyCard.jsx';
import { MeetingCard } from '../Meeting/Meetings';

const Markdown = require("react-markdown");

// TODO eventually we should not have this component existing and just have it directly in the equivalent screen

const ClubBodyDetail = (props) => {
  console.log("Received club in ClubBodyDetails", props.club);

  return (
    <div className="centerContent">
      <div className="details">
        <div className="clubHeading">
          <h1>{props.club.name}</h1>
          <button className="defaultButton contact">
            Contact
          </button>


        </div>
        <Sticky label="Scheduled meetings">
          <div className="sticky-card meeting-list">
            {props.club.events.map(event => <MeetingCard event={event} />)}
          </div>

        </Sticky>
        <Sticky label="Details">
          <div className="sticky-card">
            <Markdown source={props.club.description} />
          </div>
        </Sticky>


      </div>
    </div>
  );
};

export default ClubBodyDetail;
