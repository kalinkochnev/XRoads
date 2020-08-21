import React from "react";


import './Body.scss';

// TODO eventually we should not have this component existing and just have it directly in the equivalent screen

const ClubBodyDetail = (props) => {
  console.log("Received club in ClubBodyDetails",props.club);

  return (
    <div className="clubDetails">
      <div className="clubHeading">
        <h1>{props.club.name}</h1>
        <h2>Text @niskyrobot to 81010 to join</h2>
      </div>
      <div className="details">
        <p>
          <h2>What we do</h2>
          {props.club.description} 
        </p>
        
        <div className="clubHeading">
          <h1>FAQ</h1>
        </div>
        <p>
          <h3>Q: When do we meet?</h3>
          A: We meet twice a week, mondays and fridays under normal
          circumstances. Depending on what the situation is like, it may change
          so be sure to check back.
        </p>
        <p>
          <h3>Q: I don’t have a lot of experience, can I still join?</h3>
          A: Yeah anybody can join! You end up learning as you go. Even if you
          aren’t interested in STEM, there’s lots of other stuff you can do.
        </p>
        <p>
          <h3>Q: What language do you program your robots in?</h3>
          A: We use a set of two android phones as the brains of our robot. We
          write java to control the various motors and sensors on board.
        </p>
        <p>
          <h3>Q: What are your robots made of?</h3>
          A: We use all sorts of materials, but the main robot design is made
          from aluminum. We use 3D printed and custom parts all the time as
          well.
        </p>
      </div>
    </div>
  );
};

export default ClubBodyDetail;
