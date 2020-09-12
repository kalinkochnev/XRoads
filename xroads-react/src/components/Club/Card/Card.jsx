import React, { useState } from "react";
import "./Card.scss";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStar, faEdit } from '@fortawesome/free-regular-svg-icons'
import IconButton from '../../Common/IconButton/IconButton';
import { sendRequest } from '../../../service/xroads-api'
import { useStateValue } from "../../../service/State";

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
              <ClubIcons favorited={this.props.favorited} editable={this.props.editable} id={this.props.id} />
            </h1>
          </div>
        </div>
      </Link>
    );
  }
}

function ClubIcons(props) {
  const editable = props.editable;
  const [favorited, setFavorite] = useState(props.favorited)
  var output = [];
  const [state, dispatch] = useStateValue();


  const toggleFavorite = () => {
    let user = state.user;
    let urlArgs = {
      'districtId': user.district,
      'schoolId': user.school,
      'clubId': props.id
    }

    if (favorited) {
      sendRequest('leave_club', urlArgs, 'POST').then(response => {
        if (response.ok) {
          setFavorite(false);
          dispatch({ type: 'leave club', payload: props.id })
        }
      })
    } else {
      sendRequest('join_club', urlArgs, 'POST').then(response => {
        if (response.ok) {
          setFavorite(true);
          dispatch({ type: 'join club', payload: props.id })
        }
      })

    }
  }

  if (favorited) {
    output.push(<IconButton key={output.length + 1} icon={"faStar"} filled={true} color="goldenrod" customClickEvent={toggleFavorite} />);
  }
  else {
    output.push(<IconButton key={output.length + 1} icon={"faStar"} customClickEvent={toggleFavorite}/>);
  }

  if (editable) {
    output.push(<IconButton key={output.length + 1} icon={"faEdit"} link={`/clubs/${props.id}/edit`} />);
  }

  return output;
}

export default ClubBrowserCard;