import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenClubEdit from "./Club/Edit";
import ScreenLogin from "./User/Login";
import ScreenSignup from "./User/Signup";
import ScreenNotFound from "./Generic/NotFound";
import { ConditionalRoute } from "./Routes/ConditionalRoute";
import { clubAdminConditions, userConditions } from "./Routes/SharedConditions";
import ErrorOcurred from "./Generic/Error";

const ScreensRoot = () => {  
  return (
    <Router>
      <Switch>
        <Route exact path="/signup" component={ScreenSignup} />
        <Route exact path="/login" component={ScreenLogin} />

        <ConditionalRoute exact path="/clubs/:id/edit" component={ScreenClubEdit} condition={clubAdminConditions} conditionArgs={{modelName: "Club"}}/>
        <ConditionalRoute exact path="/clubs/:id" component={ScreenClubDetail} condition={userConditions}/>
        <ConditionalRoute exact path="/clubs" component={ScreenClubBrowser} condition={userConditions}/>
        <Route exact path="/login/school-select" component={ScreenSignup} />


        <Route exact path="/error" component={ErrorOcurred} />
        <Route component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
