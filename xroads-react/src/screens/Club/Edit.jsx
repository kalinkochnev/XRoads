import React, { useState, useEffect, Suspense } from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';
import { Slideshow, SlideshowFiller, TextSlide, ImageSlide, VideoSlide } from '../../components/Common/Slides/Slides';

import ClubEdit from '../../components/Club/Edit/Edit';

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
        <ClubEdit club={club}></ClubEdit>
      </div>
    );
  }
};


export default ScreenClubEdit;
