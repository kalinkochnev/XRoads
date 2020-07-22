import React from 'react';
<<<<<<< HEAD
import './styles/_App.scss';
import './styles/_navBars.scss';
import './styles/_searchBar.scss';
import './styles/_clubCard.scss';

var clubs = [
  ["Robotics Club", "https://unsplash.it/800/600?image=17", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["M","F"]],
  ["Drama Club", "https://unsplash.it/800/600?image=38", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["W"]],
  ["Model UN", "https://unsplash.it/800/600?image=21", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["W"]],
  ["Model UN", "https://unsplash.it/800/600?image=69", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["TH"]],
  ["Model UN", "https://unsplash.it/800/600?image=666", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["TU"]],
  ["Model UN", "https://unsplash.it/800/600?image=420", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["M","W","S"]],
];
=======
import './styles/_navBars.scss';
import './styles/_searchBar.scss';
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444

class ClubPage extends React.Component {
  constructor(props) {
    super(props);
<<<<<<< HEAD
    this.state = {
      value: null,
    };
=======
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
  }

  render() {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <div class="body">
          <SearchBar></SearchBar>
<<<<<<< HEAD
          <div class="card-container">
            {clubs.map(club => <ClubCard key={club} title={club[0]} imageURL={club[1]} description={club[2]} meetTimes={club[3]}/>)} 
          </div>
=======
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
        </div>
      </div>
    );
  }
}

class Navbar extends React.Component {
  constructor(props) {
    super(props);
<<<<<<< HEAD
    this.state = {
      value: null,
    };
=======
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
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
<<<<<<< HEAD
    this.state = {
      value: null,
    };
=======
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
  }

  render() {
    return (
<<<<<<< HEAD
      <div class="card" style={{ backgroundImage:`url(${this.props.imageURL})` }}>
        <div class="info">
          <h1>{this.props.title}</h1>
          <div class="bubble-container">
            {this.props.meetTimes.map(time => <p class="bubble" key={time}>{time}</p>)}
          </div>
          <p>{this.props.description}</p>
        </div>
      </div>
=======
      <div></div>
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
    );
  }
}

class ClubInfoPreview extends React.Component {
  constructor(props) {
    super(props);
<<<<<<< HEAD
    this.state = {
      value: null,
    };
=======
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
  }

  render() {
    return (
      <div></div>
    );
  }
}


<<<<<<< HEAD
export default ClubPage;
=======
export {ClubPage, Navbar};
>>>>>>> f6f95ef9bba80acb8598ad9a7fa9f50f3184b444
