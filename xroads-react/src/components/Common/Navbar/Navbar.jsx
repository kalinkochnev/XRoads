import React from "react";
import "./Navbar.scss";
import {removeAuthCookies} from '../../../service/xroads-api'
import { useHistory } from "react-router-dom";
import { AlertBar } from "../AlertBar/AlertBar";
import { useStateValue } from "../../../service/State";

const Navbar = () => {
  const history = useHistory();
  const [state, dispatch] = useStateValue();
  let userLoggedIn = state.user.loggedIn();
  let logout = () => {
    removeAuthCookies();
    dispatch({type: 'logout'})
    return history.replace('/login')
  }
  return (
    <div>
      <div className="navbar-simple">
        <div className="xroadsLogo">
          <h1>xroads</h1>
        </div>
        <div className="navbar-buttons">
          { userLoggedIn ? 
            <button onClick={logout}>Log Out</button> : <span></span>
          }
        </div>
      </div>
      <AlertBar>
      </AlertBar>
    </div>
    );

}

export default Navbar;