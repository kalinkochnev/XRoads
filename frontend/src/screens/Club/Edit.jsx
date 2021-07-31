import React, { useContext, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import ReactTooltip from 'react-tooltip';
import { GeneralEdit } from '../../components/Club/Edit/Edit';
import { MeetingsEdit } from '../../components/Club/Meeting/Meetings';
import Navbar from '../../components/Common/Navbar/Navbar';
import Tabs from '../../components/Common/Tabs/Tabs';
import { useStateValue } from '../../service/State';
import * as XroadsAPI from '../../service/xroads-api';
import { ClubContext } from "../Club/Routes";


// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubEdit = ({ match: { params: { clubSlug } } }) => {
  let history = useHistory();
  const [club, setClub] = useContext(ClubContext);
  const [state, dispatch] = useStateValue();
  let school = state.user.school;
  useEffect(() => {
    if (!('code' in club)) {
      history.push(`/${school}/${clubSlug}`)
    }
    XroadsAPI.fetchClubEdit(clubSlug, club.code).then(res => {
      if (res.ok) {
        res.json().then(clubRes => {
          // console.log(clubRes)

          setClub(clubRes);
        });
      } else {
        history.push(`/`)
      }
    });
  }, [clubSlug, club.code]);

  if (Object.keys(club).length == 0) {
    // console.log("Loading");
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
            <h1 data-tip="please email us support@xroads.club to change club name">{club.name + ` (${club.code})`}</h1>
            <ReactTooltip place="right" effect="solid" />
          </div>

          <Tabs>
            <div label="General">
              <GeneralEdit />
            </div>
            <div label="Meetings">
              <MeetingsEdit />
            </div>
          </Tabs>


        </div>
      </div>
    );
  }
};


export default ScreenClubEdit;
