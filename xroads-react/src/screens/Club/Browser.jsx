import React from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

import * as XroadsAPI from '../../service/xroads-api';



class ScreenClubBrowser extends React.Component {
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
        <div className="body">
          <SearchBar></SearchBar>
           <div className="card-container">
             
            {this.state.clubs.map(club => <ClubCard key={club.id} id={club.id} title={club.name} imageURL={club.main_img} description={club.description} meetTimes={["M","W","S"]}/>)} 
            </div>
        </div>
      </div>
    );
  }
}

export default ScreenClubBrowser;
