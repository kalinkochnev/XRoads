import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import LoginForm from '../../components/User/Forms/Login';
import { AlertBar, Message } from '../../components/Common/AlertBar/AlertBar';


const ScreenLogin = () => {
  let [alert, setAlert] = useState(null);

  function newAlert(type, message, dismissable = true) {
    setAlert((<Message key={1} type={type} dismissable={dismissable}>{message}</Message>))
  }

  return (
    <div>
      <Navbar></Navbar>
      <AlertBar>{alert}</AlertBar>
      <LoginForm key="1" setAlert={newAlert}></LoginForm>
    </div>
  );
}

export default ScreenLogin;
