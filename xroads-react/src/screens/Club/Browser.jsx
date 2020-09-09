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
      displayedClubs: [],
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
      displayedClubs: matchingClubs
    });

  }

  removeInvisible(clubs) {
    let editableClubsIDs = [5];
    let filteredClubs = [];

    for (let i = 0; i < clubs.length; i++) {
      if (!clubs[i].is_visible) {
        if (editableClubsIDs.includes(clubs[i].id)) {
          filteredClubs.push(clubs[i]);
        }
      } else  {
        filteredClubs.push(clubs[i]);
      }
    }
    return filteredClubs;
  }

  loadClubs() {
    // FIXME : replace the hardcoded distictId = 1, schoolId below with the actual values
    // FIXME : that should be coming in as parameters in the component
    let districtId = 1;
    let schoolId = 1;
    XroadsAPI.fetchClubs(districtId,schoolId).then( res => {
      return res.json().then( clubs => {
        clubs = this.removeInvisible(clubs);
        // clubIds - this concatenates all clubids that come back into a string
        this.setState({
          allClubs : clubs,
          displayedClubs: clubs, 
          clubIds : clubs.reduceRight( (c,a) => c.id + a, "")
        });
      });
    });
    
  }

  render() {
    const clubs = this.state.displayedClubs;
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
