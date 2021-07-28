import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import ClubCard from "../../components/Club/Card/Card";
import FeaturedCard from "../../components/Club/Featured/Featured";
import Navbar from "../../components/Common/Navbar/Navbar";
import SearchBar from "../../components/Common/Search/Search";
import { useStateValue } from "../../service/State";
import * as XroadsAPI from "../../service/xroads-api";
import checkURLParams from "../Routes/utils";

const ScreenClubBrowser = ({ match: { params } }) => {
  let history = useHistory();
  const [state, dispatch] = useStateValue();
  checkURLParams(params, { schoolSlug: "string" }, history);

  const [school, setSchool] = useState({})
  const [displayedClubs, setDisplayedClubs] = useState([]);
  let [featured, setFeatured] = useState({});

  const allClubs = school.clubs === undefined ? [] : school.clubs;
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
      let position = response.curr_featured_order;

      // Keep iterating through clubs until you find a club that is visible and is after the current featured id
      while (
        Object.keys(featured).length == 0 &&
        position <= response.clubs.length
      ) {
        function getClubByOrder(featuredOrder) {
          let clubs = response.clubs.filter(
            (club) => club.featured_order == featuredOrder
          );
          if (clubs.length == 1) {
            return clubs[0];
          }
          return null;
        }

        let club = getClubByOrder(position);

        if (club.is_visible) {
          let id = club.id;
          XroadsAPI.fetchClub(id).then((res) => {
            if (res.ok) {
              res.json().then((response) => setFeatured(response));
            }
          });
          break;
        } else {
          position++;
        }
      }
    }
  }

  function loadClubs() {
    XroadsAPI.fetchClubs(params.schoolSlug).then((res) => {
      if (res.ok) {
        return res.json().then(response => {
          console.log(response)
          setSchool(response);
          let clubs = invisibleFilter(response.clubs);
          setDisplayedClubs(clubs);
          determineFeatured(response)
        });
      } else {
        history.push("/");
      }
    });

  }

  function searchFilter(matchingIds) {
    let matchingClubs = allClubs;
    if (matchingIds.length > 0) {
      console.log(matchingIds)
      matchingClubs = matchingClubs.filter((c, i) =>
        matchingIds.includes(c.id.toString())
      );
    } else {
      matchingClubs = [];
    }
    setDisplayedClubs(matchingClubs);
  }

  useEffect(() => {
    console.log("ClubBrowser component did mount");
    if (allClubs.length === 0) {
      loadClubs();
    }
  }, [state.user.school, allClubs]);

  return (
    <div>
      <Navbar>xroads</Navbar>
      <div className="body">
        {/* <UpcomingEvents events={school.events} displayedClubs={displayedClubs}></UpcomingEvents> */}
        <FeaturedCard club={featured}></FeaturedCard>
        <SearchBar
          key={clubIds}
          clubs={allClubs}
          filterClubs={searchFilter}
        ></SearchBar>
        {displayedClubs.length == 0 ? (
            <div className="no-results">

              <h1>Ó╭╮Ò</h1>
              <h1>nothing here</h1>
            </div>) : (
            <div></div>)}
        <div className="card-container">
          {displayedClubs.length == 0 ? (
            <div>
            </div>) : (
            displayedClubs.map((club) => (
              <ClubCard
                key={club.slug}
                clubSlug={club.slug}
                title={club.name}
                imageURL={club.main_img}
                description={club.description}
                hidden={!club.is_visible}
                schoolSlug={state.user.school}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default ScreenClubBrowser;