import React from 'react';
import Navbar from '../Common/Navbar/Navbar';
const { Link } = require("react-router-dom");

const HelpNavigation = () => {
    return (
        <div>
            <Navbar>xroads</Navbar>
            <h2>I need help with: </h2>
            <ul>
                <Link to="/help/slides">Slides</Link>   

            </ul>
        </div>
    );
}

export default HelpNavigation;