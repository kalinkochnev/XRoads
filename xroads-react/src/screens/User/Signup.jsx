import React from "react";
import Navbar from "../../components/Common/Navbar/Navbar";
import SignupForm from "../../components/User/Forms/Signup";
import { Switch, Route, useRouteMatch,} from "react-router-dom";

const ScreenSignup = () => {
  let match = useRouteMatch();
  console.log(match)
  return (
    <div>
      <Navbar></Navbar>
      <Switch>
        <Route path={`${match.url}/school-selector`}>
          <h1>Not yet implemented</h1>
        </Route>
        <Route path={`${match.url}`}>
          <SignupForm></SignupForm>
        </Route>
      </Switch>
    </div>
  );
};

export default ScreenSignup;
