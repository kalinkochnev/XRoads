import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import LoginForm from '../../components/User/Forms/Login';
import { AlertBar } from '../../components/Common/AlertBar/AlertBar';


const ScreenLogin = () => {
  let [alerts, setAlerts] = useState([]);

  function addAlert(messageComponent) {
    alerts = alerts.push(messageComponent);
    setAlerts(alerts);
  }

  return (
    <div>
      <Navbar>xroads</Navbar>
      <AlertBar> {alerts.map((item) => item)}</AlertBar>
      <LoginForm addAlert={addAlert}></LoginForm>
    </div>
  );
}

export default ScreenLogin;
