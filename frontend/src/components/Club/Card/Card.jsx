import React, { useState } from "react";
import "./Card.scss";
import { Link, useHistory } from "react-router-dom";

const ClubBrowserCard = (props) => {
  var clubStyle = { backgroundImage: `url(${props.img})` };
  if (props.hidden) {
    clubStyle = { backgroundImage: `url(${props.img})`, filter: "grayscale()" }
  }

  return (
    <div className="card">
      <Link to={`/${props.schoolSlug}/${props.clubSlug}`}>
        <div className="card-content" style={clubStyle}>
          <h1>
            {props.title}
          </h1>
        </div>
      </Link>
    </div>
  );
}
export default ClubBrowserCard;