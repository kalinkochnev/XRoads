import React from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

var clubs = [
  ["Robotics Club", "https://lh3.googleusercontent.com/pw/ACtC-3fIUy1uUAK3OgwH7h4WURxF4I6vpu1K35iwDZqzBpy_hII4ySNfhqLy7yeFC5Twv9a83Rn4UvdKeZar5dhtLbRjfTsQVNhczKUy4s-CtymhzR2D19tugouYi30BX0i954NKISlQh9qYhSaq27G9JV0kNQ=w1291-h970-no?authuser=0", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["M","F"]],
  ["Drama Club", "https://unsplash.it/800/600?image=38", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["W"]],
  ["Model UN", "https://unsplash.it/800/600?image=22", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["W"]],
  ["Model UN", "https://unsplash.it/800/600?image=69", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["TH"]],
  ["Model UN", "https://unsplash.it/800/600?image=666", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["TU"]],
  ["Model UN", "https://unsplash.it/800/600?image=420", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["M","W","S"]],
];

class ScreenClubBrowser extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (  //TODO: Change the URL to actually work.
      <div>
        <Navbar>xroads</Navbar>
        <div class="body">
          <SearchBar></SearchBar>
          <a href="/page">
          <div class="card-container">
            {clubs.map(club => <ClubCard key={club} title={club[0]} imageURL={club[1]} description={club[2]} meetTimes={club[3]}/>)} 
            </div></a>
        </div>
      </div>
    );
  }
}

export default ScreenClubBrowser;
