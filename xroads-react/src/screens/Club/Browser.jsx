import React, { useContext, useEffect, useState } from 'react';

import Navbar from '../../components/Common/Navbar/Navbar';
import SearchBar from '../../components/Common/Search/Search';
import ClubCard from '../../components/Club/Card/Card';

import * as XroadsAPI from '../../service/xroads-api';
import { useStateValue } from '../../service/State';
import { Route, Switch, useHistory, useRouteMatch } from 'react-router-dom';
import checkURLParams from '../Routes/utils';
import ScreenClubDetail from './Page';
import FeaturedCard from '../../components/Club/Featured/Featured';
import UpcomingEvents from '../../components/Club/Meeting/Upcoming';

const ScreenClubBrowser = ({ match: { params } }) => {
  let history = useHistory();
  checkURLParams(params, { schoolId: "number" }, history)

  const [school, setSchool] = useState({})
  const [displayedClubs, setDisplayedClubs] = useState([]);
  let [featured, setFeatured] = useState({});

  const allClubs = school.clubs === undefined ? [] : school.clubs;
  console.log(school)
  const clubIds = displayedClubs.map(club => club.id);

  function invisibleFilter(clubs) {
    let filteredClubs = [];


    for (let i = 0; i < clubs.length; i++) {
      if (clubs[i].is_visible) {
        filteredClubs.push(clubs[i]);
      }
    }
    return filteredClubs;
  }



  function determineFeatured(response) {
    if (response.curr_featured_order != 0) {
      let position = response.curr_featured_order

      // Keep iterating through clubs until you find a club that is visible and is after the current featured id
      while (Object.keys(featured).length == 0 && position <= response.clubs.length) {
        function getClubByOrder(featuredOrder) {
          let clubs = response.clubs.filter(club => club.featured_order == featuredOrder)
          if (clubs.length == 1) {
            return clubs[0]
          }
          return null;
        }

        let club = getClubByOrder(position)

        if (club.is_visible) {
          let id = club.id
          XroadsAPI.fetchClub(id).then(res => {
            if (res.ok) {
              res.json().then(response => setFeatured(response))
            }
          })
          break
        } else {
          position++;
        }
      }
    }
  }

  function loadClubs() {
    XroadsAPI.fetchClubs(params.schoolId).then(res => {
      if (res.ok) {
        return res.json().then(response => {
          setSchool(response);
          let clubs = invisibleFilter(response.clubs);
          setDisplayedClubs(clubs);
          determineFeatured(response)
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
        <FeaturedCard club={featured}></FeaturedCard>
        <UpcomingEvents events={school.events}></UpcomingEvents>
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
