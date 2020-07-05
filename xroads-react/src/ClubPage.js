import React from 'react';
import './styles/_App.scss';
import './styles/_navBars.scss';
import './styles/_searchBar.scss';
import './styles/_clubCard.scss';

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
            <ClubCard></ClubCard>
            <ClubCard></ClubCard>
            <ClubCard></ClubCard>
            <ClubCard></ClubCard>
            <ClubCard></ClubCard>
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
      <div class="card"></div>
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
