import React, { useState, useEffect, useContext } from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';

import Tabs from '../../components/Common/Tabs/Tabs';
import { GeneralEdit, SlideshowEdit } from '../../components/Club/Edit/Edit';

import * as XroadsAPI from '../../service/xroads-api';
import { useStateValue } from '../../service/State';

// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubEdit = ({ match: { params: { clubId } } }) => {
  console.log("The club id is ", clubId);

  const [club, setClub] = useState();
  const [{ user }, dispatch] = useStateValue();

  useEffect(() => {
    XroadsAPI.fetchClub(user.district, user.school, clubId).then(res => {
      return res.json().then(clubRes => {
        setClub(clubRes);
      });
    });
  }, [clubId]);


  console.log("The useState club is", club);

  if (club == undefined) {
    console.log("Loading");
    return (
      <div>
        <Navbar>xroads</Navbar>
      </div>
    );
  }
  else {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <div className="centerContent">
          <div className="clubHeading">
            <h2>Now Editing</h2>
            <h1>{club.name}</h1>
          </div>
        <Tabs>
          <div label="General">
            <GeneralEdit label="General" club={club}></GeneralEdit>
          </div>

          <div label="Slideshow">
            <SlideshowEdit label="Slideshow" club={club}></SlideshowEdit>
          </div>

          <div label="Editors">
            There is nothing here
          </div>
        </Tabs>
        </div>
      </div>
    );
  }
};


export default ScreenClubEdit;
