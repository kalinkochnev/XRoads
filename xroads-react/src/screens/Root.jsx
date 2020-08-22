import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenLogin from "./User/Login";
import ScreenSignup from "./User/Signup";
import ScreenNotFound from "./Generic/NotFound";
import {AlertBar, Message} from '../components/Common/AlertBar/AlertBar';

const ScreensRoot = () => {
  return (
    <Router>
      <Switch>
        <Route path="/signup" component={ScreenSignup} />
        <Route exact path="/login" component={ScreenLogin} />
        <Route exact path="/clubs" component={ScreenClubBrowser} />
        <Route exact path="/clubs/:clubId" component={ScreenClubDetail} />
        <Route exact component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
