import React, { useState, useEffect, Suspense } from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';
import { Slideshow, SlideshowFiller, TextSlide, ImageSlide, VideoSlide } from '../../components/Common/Slides/Slides';

import ClubBodyDetail from '../../components/Club/Body/Body';

import * as XroadsAPI from '../../service/xroads-api';
import { useStateValue } from '../../service/State';

// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubDetail = ({ match: { params: { id } } }) => {
  const [club, setClub] = useState();
  const [state, dispatch] = useStateValue();
  let user = state.user;

  useEffect(() => {
    XroadsAPI.fetchClub(user.district, user.school, id).then(res => {
      return res.json().then(clubRes => {
        console.log("Parsed out club from endpoint", clubRes);
        setClub(clubRes);
      });
    });
  }, [id, state.user]);


  if (club == undefined) {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <SlideshowFiller />
      </div>
    );
  }
  else {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <Slideshow>
          {
            club.slides.map(slide => {
              if (slide.img) {
                return <ImageSlide key={slide.id} source={slide.img} caption={slide.text} />
              } else if (slide.video_url) {
                return <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text} />
              } else {
                return <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue" />
              }
            })
          }
        </Slideshow>
        <ClubBodyDetail club={club}></ClubBodyDetail>
      </div>
    );
  }
};


export default ScreenClubDetail;
