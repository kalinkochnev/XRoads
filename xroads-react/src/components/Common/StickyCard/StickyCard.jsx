import React, { useState } from "react";
import './StickyCard.scss';

const Sticky = (props) => {
    return (
        <div className="sticky">
            <div className="sticky-label">
                <h3>{props.label}</h3>
            </div>
            {props.children}
        </div>
    );
}
export default Sticky;