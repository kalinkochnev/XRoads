import React, { useEffect, useState } from "react";
import "./Navbar.scss";
import { AlertBar } from "../AlertBar/AlertBar";
import { Link, NavLink } from "react-router-dom";
import { useStateValue } from "../../../service/State";

const Navbar = () => {
  const [state, dispatch] = useStateValue();
  let school = state.user.school;

  return (
    <div>
      <div className="navbar-simple">
        <NavLink className="logoLink" to={`/${school}/`} >
          <div className="xroadsLogo" >
            <h1>xroads</h1>
          </div>
        </NavLink>
        {
          (school != null && school != 'undefined') &&
          <div className="navbar-buttons">
            <Link className="nav-item" to={`/${school}/edit-code/`} >
              edit club
            </Link>
          </div>
        }
      </div>
      <AlertBar>
      </AlertBar>
    </div>
  );

}

export default Navbar;