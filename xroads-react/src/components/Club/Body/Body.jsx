import React from "react";

import "./Body.scss";
const Markdown = require('react-markdown')

// TODO eventually we should not have this component existing and just have it directly in the equivalent screen

const ClubBodyDetail = (props) => {
  console.log("Received club in ClubBodyDetails", props.club);

  return (
    <div className="centerContent">
      <div className="details">
        <div className="clubHeading">
          <h1>{props.club.name}</h1>
          {/* TODO make a field that shows the how to join */}
          <h2>Text @niskyrobot to 81010 to join </h2>
        </div>
        
        <Markdown source={props.club.description}/>
      </div>
    </div>
    
  );
};

export default ClubBodyDetail;

/*
<div className="clubDetails">
      
      
    </div>
*/
