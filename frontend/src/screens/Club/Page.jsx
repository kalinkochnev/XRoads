import React, { useEffect, useState } from 'react';
import ReactNotification from 'react-notifications-component';
import 'react-notifications-component/dist/theme.css';
import { useHistory } from 'react-router-dom';
import ClubBodyDetail from '../../components/Club/Body/Body';
import { MeetingCard } from '../../components/Club/Meeting/Meetings';
import Navbar from '../../components/Common/Navbar/Navbar';
import { AutoSlide, Slideshow } from '../../components/Common/Slides/Slides';
import * as XroadsAPI from '../../service/xroads-api';


// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubDetail = ({ match: { params } }) => {
  let history = useHistory();
  console.log(params);
  const [club, setClub] = useState();

  useEffect(() => {
    XroadsAPI.fetchClub(params.clubId).then(res => {
      if (res.ok) {
        return res.json().then(clubRes => {
          console.log(clubRes)
          setClub(clubRes);
        });
      } else {
        history.push(`/school/${params.schoolId}`)
      }

    });
  }, [params.clubId]);


  if (club == undefined) {
    return (
      <div>
        <Navbar>xroads</Navbar>
      </div>
    );
  }
  else {
    return (
      <div>
        <Navbar school={params.schoolId}>xroads</Navbar>
        <ReactNotification />
        <Slideshow>
          {club.slides.map(url => <AutoSlide url={url} />)}
        </Slideshow>
        <ClubBodyDetail club={club} />
        {club.events.map(event => <MeetingCard event={event} />)}

      </div>
    );
  }
};


export default ScreenClubDetail;
