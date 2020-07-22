import React from 'react';
import { BrowserRouter as Router, BrowserRouter, Route, Switch } from "react-router-dom";
import ClubPage from './ClubPage';
import {Accounts, LoginPage, SignupPage, NotFound} from './Account';

export default function App() {
    return (
        <Switch>
            <Route exact path="/" component={ClubPage} />
            <Route path="/accounts" component={Accounts}/>
            <Route component={NotFound}/>
        </Switch>
    );
}