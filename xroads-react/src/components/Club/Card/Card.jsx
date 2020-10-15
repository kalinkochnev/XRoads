import React, { useState } from "react";
import "./Card.scss";
import { Link } from "react-router-dom";

class ClubBrowserCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }


  render() {
    var clubStyle = { backgroundImage: `url(${this.props.imageURL})` };
    if (this.props.hidden) {
      clubStyle = { backgroundImage: `url(${this.props.imageURL})`, filter: "grayscale()" }
    }
    return (
      <Link to={`/clubs/${this.props.id}`}>
        <div
          className="card"
          style={clubStyle}
        >
          <div className="info">
            <h1>
              {this.props.title}
            </h1>
          </div>
        </div>
      </Link>
    );
  }
}
export default ClubBrowserCard;