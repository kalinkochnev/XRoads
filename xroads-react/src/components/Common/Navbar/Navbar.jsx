import React from "react";
import "./Navbar.scss";
import {removeAuthCookies} from '../../../service/xroads-api'
import { useHistory } from "react-router-dom";
import { AlertBar, Message } from "../AlertBar/AlertBar";
import { useContext } from "react";
import { UserContext, User } from "../../../service/UserContext";

const Navbar = () => {
  const history = useHistory();
  let [user, setUser] = useContext(UserContext)

  let logout = () => {
    removeAuthCookies();
    setUser(prevState => {
      let user = Object.assign({}, prevState);
      Object.setPrototypeOf(user, User.prototype );
      user.logout();
      return user;
    });
    return history.replace('/login')
  }
  return (
    <div>
      <div className="navbar-simple">
        <div className="xroadsLogo">
          <h1>xroads</h1>
        </div>
        <div className="navbar-buttons">
          { user.loggedIn ? 
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