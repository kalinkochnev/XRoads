import React from 'react';
import { Navbar } from './ClubPage'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

class Accounts extends React.Component {
  render() {
    return (
      <div>
        <Navbar>xroads</Navbar>
        <div class="body">
          <h1>Testing 123</h1>
        </div>
      </div>
    );
  }
}

class LoginPage extends React.Component {

  render() {
    return (
      <div>
        <h1>Testing Login Page sdfasdf</h1>
      </div>
    );
  }
}
class SignupPage extends React.Component {

  render() {
    return (
      <div>
        <h1>Testing Signup page</h1>
      </div>
    );
  }
}

class LogoutPage extends React.Component {

  render() {
    return (
      <div>
        <h1>Testing 123</h1>
      </div>
    );
  }
}

export { Accounts, LoginPage, SignupPage };