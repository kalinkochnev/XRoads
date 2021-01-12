import React, { useState } from "react";
import "./Card.scss";
import { Link, useHistory } from "react-router-dom";

const ClubBrowserCard = (props) => {
  var clubStyle = { backgroundImage: `url(${props.imageURL})` };
  if (props.hidden) {
    clubStyle = { backgroundImage: `url(${props.imageURL})`, filter: "grayscale()" }
  }

  return (
    <Link to={`/school/${props.school}/clubs/${props.id}`}>
      <div className="card">
        <div className="card-content" style={clubStyle}>
          <h1>
            {props.title}
          </h1>
        </div>
      </div>
    </Link>
  );

}
export default ClubBrowserCard;