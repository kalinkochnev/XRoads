

import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import SignupForm from "../../components/User/Forms/Signup";
import { Switch, Route, useRouteMatch, NavLink } from "react-router-dom";
import { AlertBar } from '../../components/Common/AlertBar/AlertBar';
import { Message } from '../../components/Common/AlertBar/AlertBar'
import "../../components/Common/Common.scss";

const ScreenSignupForm = () => {
  let [alert, setAlert] = useState(null);

  function newAlert(type, message, dismissable = true) {
    setAlert((<Message key={1} type={type} dismissable={dismissable}>{message}</Message>))
  }

  return (
    <div>
      <AlertBar>{alert}</AlertBar>
      <SignupForm key="1" setAlert={newAlert}></SignupForm>
    </div>
  );

}


const ScreenSignup = () => {
  let match = useRouteMatch();
  return (
    <div>
      <Navbar></Navbar>
      <Switch>
        <Route path={`${match.url}/school-selector`}>
          <h1>Not yet implemented</h1>
        </Route>
        <Route path={`${match.url}`}>
          <ScreenSignupForm></ScreenSignupForm>
        </Route>
      </Switch>
    </div>
  );
};

export default ScreenSignup;
