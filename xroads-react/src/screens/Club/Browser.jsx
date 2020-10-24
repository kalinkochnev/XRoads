import React, { useContext, useEffect, useState } from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

import * as XroadsAPI from '../../service/xroads-api';
import { useStateValue } from '../../service/State';
import { Route, Switch, useHistory, useRouteMatch } from 'react-router-dom';
import checkURLParams from '../Routes/utils';
import ScreenClubDetail from './Page';

const ScreenClubBrowser = ({ match: { params } }) => {
  let history = useHistory();

  checkURLParams(params, { schoolId: "number" }, history)

  const [allClubs, setAllClubs] = useState([]);
  const [displayedClubs, setDisplayedClubs] = useState([]);
  const clubIds = allClubs.map(club => club.id);

  function invisibleFilter(clubs) {
    let filteredClubs = [];


    for (let i = 0; i < clubs.length; i++) {
      if (clubs[i].is_visible) {
        filteredClubs.push(clubs[i]);
      }
    }
    return filteredClubs;
  }

  function loadClubs() {
    XroadsAPI.fetchClubs(params.schoolId).then(res => {
      if (res.ok) {
        return res.json().then(response => {
          console.log(response)
          let clubs = invisibleFilter(response.clubs);
          setAllClubs(clubs);
          setDisplayedClubs(clubs);
        });
      } else {
        history.push('/')
      }
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
  }, [params.school])

  return (
    <div>
      <Navbar>xroads</Navbar>
      <div className="body">
        <SearchBar key={clubIds} clubs={allClubs} filterClubs={searchFilter}></SearchBar>
        <div className="card-container">
          {
            displayedClubs.length == 0 ? (<h1>Loading...</h1>) :
              displayedClubs.map(club => <ClubCard
                key={club.id}
                id={club.id}
                title={club.name}
                imageURL={club.main_img}
                description={club.description}
                hidden={!club.is_visible}
                school={params.schoolId}
              />)
          }

        </div>
      </div>
    </div>
  );
}

export default ScreenClubBrowser;
