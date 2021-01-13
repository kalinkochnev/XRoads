import React, { useState } from "react";
import './StickyCard.scss';

const Sticky = (props) => {
  return (
      <div className="sticky">
        <div className="sticky-label">
            <p>{props.label}</p>
        </div>
        {props.children}
      </div>
  );
}
export default Sticky;