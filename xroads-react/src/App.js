import React from 'react';
import { BrowserRouter as Router, BrowserRouter, Route } from "react-router-dom";
import ClubPage from './ClubPage';
import LoginPage from './Login';

export default function App() {
    return (
        <BrowserRouter>
            <Route exact path="/" component={ClubPage} />
            <Route exact path="/testing123" component={LoginPage}/>
        </BrowserRouter>
    );
}