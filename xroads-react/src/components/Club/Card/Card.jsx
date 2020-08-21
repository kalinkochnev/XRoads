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
        <div className="card" style={{ backgroundImage:`url(${this.props.imageURL})` }}>
          <div className="info">
            <h1>{this.props.title}</h1>
            <div className="bubble-container">
              {this.props.meetTimes.map(time => <p className="bubble" key={time}>{time}</p>)}
            </div>
            <p>{this.props.description}</p>
          </div>
        </div>
      );
    }
  }

export default ClubBrowserCard;