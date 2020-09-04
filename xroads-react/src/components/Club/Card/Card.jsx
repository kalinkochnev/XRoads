import React from 'react';
import './Card.scss';

class ClubBrowserCard extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        value: null,
      };
    }
  
    render() {
      return (
        <a href={`/clubs/${this.props.id}`}>
          <div className="card" style={{ backgroundImage:`url(${this.props.imageURL})` }}>
            <div className="info">
              <h1>{this.props.title}</h1>
              <p>{this.props.description}</p>
            </div>
          </div>
        </a>
      );
    }
  }

export default ClubBrowserCard;