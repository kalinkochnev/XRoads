import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import SignupForm from "../../components/User/Forms/Signup";
import { Switch, Route, useRouteMatch, } from "react-router-dom";
import { AlertBar, Message } from '../../components/Common/AlertBar/AlertBar';


const ScreenSignupForm = () => {
  let [alerts, setAlert] = useState([]);

  function addAlert(oldAlerts, newAlert) {
    return oldAlerts.concat([newAlert]);
  }


  return (
    <div>
      <AlertBar>
        {alerts.map((item) => item)}
      </AlertBar>
      <button onClick={() => setAlert(alert => addAlert(alert))}>sdfsdfsdfsdf</button>
      <SignupForm key="1" addAlert={(newAlert) => setAlert(alert => addAlert(alert, newAlert))}></SignupForm>
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
