import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import LoginForm from '../../components/User/Forms/Login';
import { AlertBar, Message } from '../../components/Common/AlertBar/AlertBar';


const ScreenLogin = () => {
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
      <Navbar></Navbar>
      <AlertBar>
        {alerts.map((item) => item)}
      </AlertBar>
      <LoginForm key="1" addAlert={addAlert}></LoginForm>
    </div>
  );
}

export default ScreenLogin;
