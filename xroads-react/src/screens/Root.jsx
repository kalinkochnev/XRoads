import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenLogin from "./User/Login";
import ScreenSignup from "./User/Signup";
import ScreenNotFound from "./Generic/NotFound";
import { AuthRoute } from "./Routes/AuthenticatedRoute";
import { useContext } from "react";
import {UserContext} from '../service/UserContext';

const ScreensRoot = () => {
  let user = useContext(UserContext);
  
  return (
    <Router>
      <Switch>
        <Route path="/signup" component={ScreenSignup} />
        <Route exact path="/login" component={ScreenLogin} />

        <AuthRoute exact path="/clubs" component={ScreenClubBrowser} auth={user.loggedIn}/>
        <AuthRoute exact path="/clubs/:clubId" component={ScreenClubDetail} auth={user.loggedIn}/>

        <Route exact component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
