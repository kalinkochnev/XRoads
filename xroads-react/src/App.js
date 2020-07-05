import React from 'react';
import { BrowserRouter as Router, BrowserRouter, Route, Switch } from "react-router-dom";
import {ClubPage} from './ClubPage';
import {Accounts, LoginPage, SignupPage} from './Account';

export default function App() {
    return (
        <Switch>
            <Route exact path="/" component={ClubPage} />
            <Route exact path="/accounts" component={Accounts}/>
            
        </Switch>
    );
}