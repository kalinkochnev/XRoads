import React from "react";
import "./Navbar.scss";
import {removeAuthCookies} from '../../../service/xroads-api'
import { useHistory } from "react-router-dom";
import { AlertBar, Message } from "../AlertBar/AlertBar";
import { useContext } from "react";
import { UserContext } from "../../../service/UserContext";

const Navbar = () => {
  const history = useHistory();
  let [user, setUser] = useContext(UserContext)

  let logout = () => {
    removeAuthCookies();
    setUser(prevState => {
      let user = Object.assign({}, prevState);
      user.loggedIn = false
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
          <button onClick={logout}>logout</button>
        </div>
      </div>
      {/*<AlertBar>
        <Message type="info">I AM  T E X T asdk fklsdajf lksdalfk sdalfkljsadjklf askjlsakljf jlksdafalkj sadkljfkj lsdals kjdlkjk jlfkljalk jsadlkj flds kljajklf aslkf lkjas kla</Message>
      </AlertBar>*/}
    </div>
    );

}

export default Navbar;