import React, { useState, useEffect, useContext } from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';

import Tabs from '../../components/Common/Tabs/Tabs';
import { GeneralEdit, SlideshowEdit } from '../../components/Club/Edit/Edit';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faQuestionCircle } from '@fortawesome/free-regular-svg-icons';

import ReactTooltip from 'react-tooltip';

import * as XroadsAPI from '../../service/xroads-api';
import { useStateValue } from '../../service/State';

import ReactNotification from 'react-notifications-component'
import 'react-notifications-component/dist/theme.css'
import { store } from 'react-notifications-component';


// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubEdit = ({ match: { params: { id } } }) => {

  const [club, setClub] = useState();
  const [{ user }, dispatch] = useStateValue();

  useEffect(() => {
    XroadsAPI.fetchClub(user.district, user.school, id).then(res => {
      return res.json().then(clubRes => {
        setClub(clubRes);
      });
    });
  }, [id, user]);


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
        <ReactNotification />
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
