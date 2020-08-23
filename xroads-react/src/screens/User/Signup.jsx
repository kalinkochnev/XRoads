import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import SignupForm from "../../components/User/Forms/Signup";
import { Switch, Route, useRouteMatch, } from "react-router-dom";
import { AlertBar } from '../../components/Common/AlertBar/AlertBar';
import { Message } from '../../components/Common/AlertBar/AlertBar'

const ScreenSignupForm = () => {
  let [alerts, setAlert] = useState([]);

  function addAlert(type, message, dismissable = true) {
    // WARNING do not modify the order of the array or else you should not be using this key value!
    setAlert((oldAlerts) => {
      let msgComponent = (<Message key={oldAlerts.length + 1} type={type} dismissable={dismissable}>{message}</Message>)
      return oldAlerts.concat([msgComponent])
    })
  }

  return (
    <div>
      <AlertBar>
        {alerts.map((item) => item)}
      </AlertBar>
      <SignupForm key="1" addAlert={addAlert}></SignupForm>
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
