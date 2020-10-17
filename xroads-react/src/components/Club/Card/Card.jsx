import React, { useState } from "react";
import "./Card.scss";
import { Link, useHistory } from "react-router-dom";

const ClubBrowserCard = (props) => {
  let history = useHistory()

  var clubStyle = { backgroundImage: `url(${props.imageURL})` };
  if (props.hidden) {
    clubStyle = { backgroundImage: `url(${props.imageURL})`, filter: "grayscale()" }
  }

  return (
    <Link to={`/school/${props.school}/clubs/${props.id}`}>
      <div
        className="card"
        style={clubStyle}
      >
        <div className="info">
          <h1>
            {props.title}
          </h1>
        </div>
      </div>
    </Link>
  );

}
export default ClubBrowserCard;