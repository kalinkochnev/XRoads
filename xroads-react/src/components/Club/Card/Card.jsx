import React from "react";
import "./Card.scss";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar, faEdit } from '@fortawesome/free-regular-svg-icons'
import { faStar as faStarFilled } from '@fortawesome/free-solid-svg-icons'


class ClubBrowserCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (
      <Link to={`/clubs/${this.props.id}`}>
        <div
          className="card"
          style={{ backgroundImage: `url(${this.props.imageURL})` }}
        >
          <div className="info">
            <h1>
              {this.props.title}
              <ClubIcons favorited={true} editable={true}/>
            </h1>
          </div>
        </div>
      </Link>
    );
  }
}

function ClubIcons(props) {
  const editable = props.editable;
  const favorited = props.favorited;
  var output = [];

  if (favorited) {
    output.push(<FontAwesomeIcon className="star filled" icon={faStarFilled} />);
  }
  else {
    output.push(<FontAwesomeIcon className="star" icon={faStar} />);
  }

  if (editable) {
    output.push(<FontAwesomeIcon className="edit" icon={faEdit} />);
  }

  return output;
}

export default ClubBrowserCard;