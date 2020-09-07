import React from "react";
import Linkify from "react-linkify"

import "./Body.scss";
const Markdown = require('react-markdown')

// TODO eventually we should not have this component existing and just have it directly in the equivalent screen

const ClubBodyDetail = (props) => {
  console.log("Received club in ClubBodyDetails", props.club);

  return (
    <div className="clubBody">
      <div className="details">
        <div className="clubHeading">
          <h1>{props.club.name}</h1>

          <Linkify><h2> {props.club.join_promo}</h2></Linkify>
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
