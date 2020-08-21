import React from 'react';
import Navbar from '../../components/Common/Navbar/Navbar';
import { Slideshow, TextSlide, ImageSlide, VideoSlide } from '../../components/Common/Slides/Slides';
import ClubBodyDetail from '../../components/Club/Body/Body';

// This page is going to use the react hooks format: https://reactjs.org/docs/hooks-overview.html
// This: { match: { params: { id }}} is the same as props.match.params.id and you can refer to id directly later
const ScreenClubDetail = ({ match: {  params: { id }}}) => {
  return (
    <div>
      <Navbar>xroads</Navbar>
      <Slideshow>
        <ImageSlide
          source="https://lh3.googleusercontent.com/pw/ACtC-3dTHcR7fGDF02Z4rAWarD_Jek_kbVPCL6WzU4iju57ePIN2W1bd-uhWUi8yVW4dStChrDK2fdSmTo7R7e4PTSi-aEV4PROwsf7eqp8sFiSOnuxQGaj2qCfr198pxY6H9TR0YpJw2RLXkBpz0Ec-jxjX7w=w1291-h969-no?authuser=0"
          caption="Our driving team and robot (bottom left) just before the begining of the match."
        />
        <TextSlide
          title="We compete in the FTC"
          body="Each year, more than 7,000 high school teams around the world go head to head in the First Tech Challenge. The competition changes each year, keeping teams on their toes."
          color="lightblue"
        />
        <ImageSlide
          source="https://lh3.googleusercontent.com/Hh7-xwoD3hz1g6SZ_MXnCeuFveffb9IU0nc6R3eot76xFFNo6To2v6Jzy2vHsSbrA4K3aVQWkYXqk7BWsLks6DXn0ivb2KhKBRgQ9Q_56hXzqmkQWDUZIMgJLQ0_TEah6U6hIgb8yky_PXTERAE0XUAKyCmwzvOCYOzOIxmZr3_mFggYcNpFR9uKpOLEys3uBj68EC3RwRPrd5idynC-vOoFVsbuiasaN0Hl13NnR3gYB4ORmV0WzzNU-gPEhHFTDn4wqEkDWjZyfRlGdAp0em3jS02awHBXtti7t4bmY971Ldy0mN8OrkH4FWS1Qt1th87Tip2eh960IbsufQSU5zD5byrBkou_I30RAMYhQgPiGDMByc87Pq8hRGdKhuW2JVgApYncJxjGq3MMOTLlzCrGiRw5DAvSeqJDZw5PLu2VDQxV53c_DjP-FNrF95sZmLyb71x5B5H2ShXZK5GGnWx-WhRIAT9F86Z-S2c4qHCwdp04T_9DUZmUQDJ5mOtbPIY4xgl5X1OdxowM80q2HBQB5WPJOj7P6l1Fd11HF1LApipLBBnIhmVAMX6sAPzuhP7qrAtaaJYVRPGVwNeA1yYJSYUOU86P4WFN9xrAJvz0R0-jECciEeokyOXySLkBKiUypg_f5tlWVzHMXSrbkXQfaU6eTLFD39PVF7kgBN6xqWH1f6sX0kD0Bx_ntg=w1785-h1340-no?authuser=0"
          caption="Sam describes his innovative duct tape and nylon cord intake to a skeptical team."
        />
        <TextSlide
          title="What we're about"
          body="Robotics is a great way to put all those STEM skills from class to a good use. But it's more than that too. It's about creative thinking and problem solving under pressure."
          color="#ffc4c4"
        />
        <VideoSlide
          videoURL="https://www.youtube.com/watch?v=D2-CRBoGpJQ"
          caption="Here's our challenge kickoff from our past season."
        />
      </Slideshow>
      <ClubBodyDetail></ClubBodyDetail> 
    </div> 
  );
};

export default ScreenClubDetail;
