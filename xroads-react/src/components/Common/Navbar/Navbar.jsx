import React from "react";
import "./Navbar.scss";
import {removeAuthCookies} from '../../../service/xroads-api'
import { useHistory } from "react-router-dom";

const Navbar = () => {
  const history = useHistory();

  let logout = () => {
    removeAuthCookies();
    return history.replace('/login')
  }
  return (
      <div className="navbar-simple">
        <div className="xroadsLogo">
          <h1>xroads</h1>
        </div>
        <div className="navbar-buttons">
          <button onClick={logout}>logout</button>
        </div>
      </div>
    );

}

export default Navbar;