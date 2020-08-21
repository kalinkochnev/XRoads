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
        <div class="card" style={{ backgroundImage:`url(${this.props.imageURL})` }}>
          <div class="info">
            <h1>{this.props.title}</h1>
            <div class="bubble-container">
              {this.props.meetTimes.map(time => <p class="bubble" key={time}>{time}</p>)}
            </div>
            <p>{this.props.description}</p>
          </div>
        </div>
      );
    }
  }

export default ClubBrowserCard;