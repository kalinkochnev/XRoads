import React from 'react';
import './styles/_navBars.scss';
import './styles/_searchBar.scss';
import './styles/_clubCard.scss';

import * as XroadsAPI from './service/xroads-api';



class ClubBrowser extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      clubs: [],
    };

    this.getClubs = this.getClubs.bind(this);
  }

  componentDidMount() {
    console.log("ClubBrowser component did mount");
    this.getClubs()
  }

  getClubs() {
    XroadsAPI.fetchClubs().then( res => {
      console.log("Received res from club endpoint", res);
      return res.json().then( clubs => {
        console.log("Parsed out clubs from endpoint", clubs);
        this.setState(() => ({
          clubs: clubs
        }));
      });
    });
    
  }

  render() {
    return (  //TODO: Change the URL to actually work.
      <div>
        <Navbar>xroads</Navbar>
        <div class="body">
          <SearchBar></SearchBar>
           <div class="card-container">
             
            {this.state.clubs.map(club => <ClubCard key={club.id} id={club.id} title={club.name} imageURL={club.main_img} description={club.description} meetTimes={["M","W","S"]}/>)} 
            </div>
        </div>
      </div>
    );
  }
}

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (
      <div class="navbar-simple">
        <div class="xroadsLogo"><h1>xroads</h1></div>
        <div class="navbar-buttons">
          <button>logout</button>
        </div>
      </div>
    );
  }
}

class SearchBar extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <form class="default-searchbar">
          <input type="text" id="search-box" placeholder="Search for clubs..."></input>
          <input id="search-submit" type="submit" value=""></input>
        </form>
      </div>

    );
  }
}

class ClubCard extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (
      <a href={`/club/${this.props.id}`} >
        <div class="card" style={{ backgroundImage:`url(${this.props.imageURL})` }}>
          <div class="info">
            <h1>{this.props.title}</h1>
            <div class="bubble-container">
              {this.props.meetTimes.map(time => <p class="bubble" key={time}>{time}</p>)}
            </div>
            <p>{this.props.description}</p>
          </div>
        </div>
      </a>
    );
  }
}

class ClubInfoPreview extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (
      <div></div>
    );
  }
}


export {ClubBrowser, Navbar};
