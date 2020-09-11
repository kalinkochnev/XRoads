import React, { useState, useEffect } from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';

import Tabs from '../../components/Common/Tabs/Tabs';
import { GeneralEdit, SlideshowEdit } from '../../components/Club/Edit/Edit';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle } from '@fortawesome/free-regular-svg-icons';

import ReactTooltip from 'react-tooltip';

import * as XroadsAPI from '../../service/xroads-api';

// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubEdit = ({ match: { params: { clubId } } }) => {
  console.log("The club id is ", clubId);

  const [club, setClub] = useState();
  useEffect(() => {
    // FIXME : replace the hardcoded districtId and schoolId below
    // with the information from the user's profile
    let districtId = 1;
    let schoolId = 1;

    XroadsAPI.fetchClub(districtId, schoolId, clubId).then(res => {
      console.log("Received res from club endpoint", res);
      return res.json().then(clubRes => {
        console.log("Parsed out club from endpoint", clubRes);
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
            <h1 data-tip="please email us support@xroads.club to change club name">{club.name}</h1>
            <ReactTooltip place="right" effect="solid"/>
          </div>
          <Tabs>
            <div label="General">
              <GeneralEdit label="General" club={club}></GeneralEdit>
            </div>

            <div label="Slideshow">
              <SlideshowEdit label="Slideshow" club={club}></SlideshowEdit>
            </div>

            <div label="Editors">
              <p data-tip="please email us support@xroads.club to change club name">There is nothing here</p>
            </div>
          </Tabs>
        </div>
      </div>
    );
  }
};


export default ScreenClubEdit;
