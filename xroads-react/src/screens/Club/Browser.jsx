import React from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

import * as XroadsAPI from '../../service/xroads-api';



class ScreenClubBrowser extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      allClubs: [],
      clubs: [],
      clubIds: "",
    };

    this.loadClubs = this.loadClubs.bind(this);
    this.filterClubs = this.filterClubs.bind(this);
  }

  componentDidMount() {
    console.log("ClubBrowser component did mount");
    this.loadClubs()
  }

  filterClubs(matchingClubIds) {
    let matchingClubs = this.state.allClubs;
    if (matchingClubIds.length > 0) {
      matchingClubs = this.state.allClubs.filter( (c,i) => matchingClubIds.includes(c.id.toString()) );
    } else {
      matchingClubs = [];
    }

    this.setState({
      clubs: matchingClubs
    });

  }

  loadClubs() {
    // FIXME : replace the hardcoded distictId = 1, schoolId below with the actual values
    // FIXME : that should be coming in as parameters in the component
    let districtId = 1;
    let schoolId = 1;
    XroadsAPI.fetchClubs(districtId,schoolId).then( res => {
      console.log("Received res from club endpoint", res);
      return res.json().then( clubs => {
        console.log("Parsed out clubs from endpoint", clubs);
        // clubIds - this concatenates all clubids that come back into a string
        this.setState({
          allClubs : clubs,
          clubs: clubs, 
          clubIds : ""// clubs.reduceRight( (c,a) => c.id + a, "")
        });
      });
    });
    
  }

  render() {
    const clubs = this.state.clubs;
    return (  //TODO: Change the URL to actually work.
      
      <div>
        <Navbar>xroads</Navbar>
        <div className="body">
          <SearchBar key={this.state.clubIds} clubs={clubs} filterClubs={this.filterClubs}></SearchBar>
           <div className="card-container">
            {
              clubs.map(club => <ClubCard key={club.id} id={club.id} title={club.name} imageURL={club.main_img} description={club.description} meetTimes={["M","W","S"]}/>)
            } 
            </div>
        </div>
      </div>
    );
  }
}

export default ScreenClubBrowser;
