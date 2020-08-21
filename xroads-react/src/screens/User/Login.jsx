import React from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import LoginForm from '../../components/User/Forms/Login';

class ScreenLogin extends React.Component {
  render() {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <LoginForm></LoginForm>
      </div>
    );
  }
}

export default ScreenLogin;
