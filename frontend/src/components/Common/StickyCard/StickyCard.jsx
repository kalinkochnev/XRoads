import React, { useState } from "react";
import './StickyCard.scss';

const Sticky = (props) => {
    return (
        <div className="sticky">
            <div className="sticky-label">
                {props.label}
            </div>
            {props.children}
        </div>
    );
}
export default Sticky;