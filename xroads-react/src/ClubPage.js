import React from 'react';
import './styles/_App.scss';
import './styles/_navBars.scss';
import './styles/_searchBar.scss';
import './styles/_clubCard.scss';

var clubs = [
  ["Robotics Club", "https://unsplash.it/800/600?image=58"],
  ["Drama Club", "https://unsplash.it/800/600?image=61"],
  ["Model UN", "https://unsplash.it/800/600?image=63"],
  ["Model UN", "https://unsplash.it/800/600?image=69"],
  ["Model UN", "https://unsplash.it/800/600?image=61"],
  ["Model UN", "https://unsplash.it/800/600?image=66"],
];

class ClubPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <div class="body">
          <SearchBar></SearchBar>
          <div class="card-container">
            {clubs.map(club => <ClubCard key={club} title={club[0]} imageURL={club[1]} />)} 
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
      <div class="card" style={{ backgroundImage:`url(${this.props.imageURL})` }}>
        <div class="info">
          <h1>{this.props.title}</h1>
        </div>
      </div>
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


export default ClubPage;
