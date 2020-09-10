import React, { useContext, useEffect, useState } from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

import * as XroadsAPI from '../../service/xroads-api';
import { UserContext } from '../../service/UserContext';

const ScreenClubBrowser = () => {
  const [allClubs, setAllClubs] = useState([]);
  const [displayedClubs, setDisplayedClubs] = useState([]);
  const clubIds = allClubs.map(club => club.id);
  let [user, setUser] = useContext(UserContext);


  function invisibleFilter(clubs) {
    let editableClubs = user.editableClubs;
    let filteredClubs = [];

    for (let i = 0; i < clubs.length; i++) {
      if (!clubs[i].is_visible) {
        if (editableClubs.includes(clubs[i].id)) {
          filteredClubs.push(clubs[i]);
        }
      } else {
        filteredClubs.push(clubs[i]);
      }
    }
    return filteredClubs;
  }

  function loadClubs() {
    // FIXME : replace the hardcoded distictId = 1, schoolId below with the actual values
    // FIXME : that should be coming in as parameters in the component
    let districtId = 1;
    let schoolId = 1;
    XroadsAPI.fetchClubs(districtId, schoolId).then(res => {
      return res.json().then(clubs => {
        clubs = invisibleFilter(clubs);
        setAllClubs(clubs);
        setDisplayedClubs(clubs);
      });
    });

  }

  function searchFilter(matchingIds) {
    let matchingClubs = allClubs;
    if (matchingIds.length > 0) {
      matchingClubs = matchingClubs.filter((c, i) => matchingIds.includes(c.id.toString()));
    } else {
      matchingClubs = [];
    }
    setDisplayedClubs(matchingClubs);
  }


  useEffect(() => {
    console.log("ClubBrowser component did mount");
    loadClubs();
  }, [])

  return (
    <div>
      <Navbar>xroads</Navbar>
      <div className="body">
        <SearchBar key={clubIds} clubs={allClubs} filterClubs={searchFilter}></SearchBar>
        <div className="card-container">
          {
            displayedClubs.map(club => <ClubCard key={club.id} id={club.id} title={club.name} imageURL={club.main_img} description={club.description} meetTimes={["M", "W", "S"]} />)
          }
        </div>
      </div>
    </div>
  );
}

export default ScreenClubBrowser;
