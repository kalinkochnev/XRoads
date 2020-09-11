import React from "react";
import "./Card.scss";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar, faEdit } from '@fortawesome/free-regular-svg-icons'
import IconButton from '../../Common/IconButton/IconButton';

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
              <ClubIcons favorited={true} editable={true} id={this.props.id}/>
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
    output.push(<IconButton icon={"faStar"} filled={true} color="goldenrod" customClickEvent={""/*Whatever*/} />);
  }
  else {
    output.push(<IconButton icon={"faStar"} customClickEvent={""/*Whatever*/} />);
  }

  if (editable) {
    output.push(<IconButton icon={"faEdit"}link={`/clubs/${props.id}/edit`} />);
  }

  return output;
}

export default ClubBrowserCard;