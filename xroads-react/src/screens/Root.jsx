import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenClubEdit from "./Club/Edit";
import ScreenLogin from "./User/Login";
import ScreenSignup from "./User/Signup";
import ScreenNotFound from "./Generic/NotFound";
import { AuthRoute } from "./Routes/AuthenticatedRoute";
import { CanEditRoute } from "./Routes/UserCanEdit";
import { ConditionalRoute } from "./Routes/ConditionalRoute";
import { userConditions } from "./Routes/SharedConditions";
import ErrorOcurred from "./Generic/Error";

const ScreensRoot = () => {  
  return (
    <Router>
      <Switch>
        <Route exact path="/signup" component={ScreenSignup} />
        <Route exact path="/signup/school-select" component={ScreenSignup} />
        <Route exact path="/login" component={ScreenLogin} />

        <ConditionalRoute exact path="/clubs/:id" component={ScreenClubDetail} condition={userConditions}/>
        <ConditionalRoute exact path="/clubs" component={ScreenClubBrowser} condition={userConditions}/>
        <CanEditRoute exact path="/clubs/:id/edit" component={ScreenClubEdit} modelName="Club"/>
        
        <Route exact path="/error" component={ErrorOcurred} />
        <Route component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
