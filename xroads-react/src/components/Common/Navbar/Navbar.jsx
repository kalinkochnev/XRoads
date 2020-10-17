import React, { useEffect, useState } from "react";
import "./Navbar.scss";
import { AlertBar } from "../AlertBar/AlertBar";
import { NavLink } from "react-router-dom";

const Navbar = (props) => {
  return (
    <div>
      <div className="navbar-simple">
        <NavLink className="logoLink" to={`/school/${props.school}/`} >
          <div className="xroadsLogo" >
            <h1>xroads</h1>
          </div>
        </NavLink>
        <div className="navbar-buttons">
          <span></span>
        </div>
      </div>
      <AlertBar>
      </AlertBar>
    </div>
  );

}

export default Navbar;