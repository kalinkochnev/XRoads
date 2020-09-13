import React, { useState } from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import LoginForm from '../../components/User/Forms/Login';
import { AlertBar, Message } from '../../components/Common/AlertBar/AlertBar';
import "../../components/Common/Common.scss";
import SchoolSelectForm from "../../components/User/Forms/SchoolSelect";


const SchoolSelectScreen = () => {
  let [alert, setAlert] = useState(null);

  function newAlert(type, message, dismissable = true) {
    setAlert((<Message key={1} type={type} dismissable={dismissable}>{message}</Message>))
  }

  return (
    <div>
      <AlertBar>{alert}</AlertBar>
      <SchoolSelectForm key="1" setAlert={newAlert}></SchoolSelectForm>
    </div>
  );
}

export default SchoolSelectScreen;
