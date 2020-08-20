import React from 'react';
import { BrowserRouter as Router, BrowserRouter, Route, Switch } from "react-router-dom";
import {ClubBrowser} from './ClubBrowser';
import {ClubPage} from './ClubPage';
import {Accounts, LoginPage, SignupPage, NotFound} from './Account';

export default function App() {
    return (
        <Switch>
            <Route exact path="/" component={ClubBrowser} />
            <Route path="/accounts" component={Accounts}/>
            <Route path="/club/:clubId" component={ClubPage}/>
            <Route component={NotFound}/>
        </Switch>
    );
}