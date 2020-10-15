import React from "react";
import "./Navbar.scss";
import { AlertBar } from "../AlertBar/AlertBar";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <div>
      <div className="navbar-simple">
        <NavLink className="logoLink" to="/clubs">
          <div className="xroadsLogo">
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