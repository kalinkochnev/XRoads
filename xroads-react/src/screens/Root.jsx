import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenLogin from "./User/Login";
import ScreenSignup from "./User/Signup";
import ScreenNotFound from "./Generic/NotFound";
import { AuthRoute } from "./Routes/AuthenticatedRoute";

const ScreensRoot = () => {  
  return (
    <Router>
      <Switch>
        <Route exact path="/signup" component={ScreenSignup} />
        <Route exact path="/login" component={ScreenLogin} />

        <AuthRoute exact path="/clubs/:clubId" component={ScreenClubDetail} />
        <AuthRoute exact path="/clubs" component={ScreenClubBrowser} />

        <Route component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
