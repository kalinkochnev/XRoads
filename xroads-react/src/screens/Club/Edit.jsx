import React, { useState, useEffect, useContext } from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';

import Tabs from '../../components/Common/Tabs/Tabs';
import { EditAccess, GeneralEdit, ManageQuestions, SlideshowEdit } from '../../components/Club/Edit/Edit';

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
const ScreenClubEdit = ({ match: { params: { school, id } } }) => {
  const [club, setClub] = useState();
  const [state, dispatch] = useStateValue();

  useEffect(() => {
    XroadsAPI.fetchClub(id).then(res => {
      return res.json().then(clubRes => {
        setClub(clubRes);
      });
    });
  }, [id]);

  if (club == undefined) {
    console.log("Loading");
    return (
      <div>
        <Navbar school={school}>xroads</Navbar>
      </div>
    );
  }
  else {
    return (
      <div>
        <Navbar school={school}>xroads</Navbar>
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
          </Tabs>
        </div>
      </div>
    );
  }
};


export default ScreenClubEdit;
