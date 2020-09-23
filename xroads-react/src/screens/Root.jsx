import React from "react";
import { BrowserRouter as Router, Route, Switch} from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenClubEdit from "./Club/Edit";
import ScreenLogin from "./User/Login";
import ScreenSignup from "./User/Signup";
import ScreenNotFound from "./Generic/NotFound";
import { ConditionalRoute } from "./Routes/ConditionalRoute";
import { clubAdminConditions, registrationConditions, userConditions } from "./Routes/SharedConditions";
import ErrorOcurred from "./Generic/Error";
import SchoolSelectForm from "../components/User/Forms/SchoolSelect";
import SchoolSelectScreen from "./User/SchoolSelect";
import ScreensHome from "./Home";
import CarouselBug from "./CarouselBug";

const ScreensRoot = () => {  
  return (
    <Router>

        <Route exact path="/" component={ScreensHome} />
        <Route exact path="/carouselbug" component={CarouselBug} />
        <Route exact path="/signup" component={ScreenSignup} />
        <Route exact path="/login" component={ScreenLogin} />

        <ConditionalRoute exact path="/clubs/:id/edit" component={ScreenClubEdit} condition={clubAdminConditions} conditionArgs={{modelName: "Club"}}/>
        <ConditionalRoute exact path="/clubs/:id" component={ScreenClubDetail} condition={userConditions}/>
        <ConditionalRoute exact path="/clubs" component={ScreenClubBrowser} condition={userConditions}/>
        <ConditionalRoute exact path="/login/school-select" component={SchoolSelectScreen} condition={registrationConditions} />


        <Route exact path="/error" component={ErrorOcurred} />
        {/* <Route component={ScreenNotFound} /> */}

    </Router>
  );
};

export default ScreensRoot;
