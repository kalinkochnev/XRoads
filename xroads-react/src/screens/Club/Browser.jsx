import React, { useContext, useEffect, useState } from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

import * as XroadsAPI from '../../service/xroads-api';
import { useStateValue } from '../../service/State';

const ScreenClubBrowser = () => {
  const [allClubs, setAllClubs] = useState([]);
  const [displayedClubs, setDisplayedClubs] = useState([]);
  const clubIds = allClubs.map(club => club.id);
  const [state, dispatch] = useStateValue();

  function invisibleFilter(clubs) {
    let editableClubs = state.user.editableClubs(state.user.roles)
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

    XroadsAPI.fetchClubs(state.user.district, state.user.school).then(res => {
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
  }, [state.user])

  return (
    <div>
      <Navbar>xroads</Navbar>
      <div className="body">
        <SearchBar key={clubIds} clubs={allClubs} filterClubs={searchFilter}></SearchBar>
        <div className="card-container">
          {
            displayedClubs.map(club => 
              <ClubCard 
                key={club.id} 
                id={club.id} 
                title={club.name} 
                imageURL={club.main_img} 
                description={club.description}
                favorited={club}
                editable={state.user.editableClubs(state.user.roles).includes(club.id)}
                hidden={!club.is_visible}
              />
            )
          }
        </div>
      </div>
    </div>
  );
}

export default ScreenClubBrowser;
