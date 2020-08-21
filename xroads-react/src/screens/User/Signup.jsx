import React from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import SignupForm from '../../components/User/Forms/Signup';

class ScreenSignup extends React.Component {
  render() {
    return (
      <div>
        <Navbar></Navbar>
        <SignupForm></SignupForm>
      </div>
    );
  }
}

export default ScreenSignup;
