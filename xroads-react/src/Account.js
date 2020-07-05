import React from 'react';
import { Navbar } from './ClubPage'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

class NotFound extends React.Component {
  render() {
    return (
      <h1>this page was not found</h1>
    );
  }
}

class Accounts extends React.Component {
  render() {
    const {path} = this.props.match;

    return (
      <div>
        <Navbar>xroads</Navbar>
        <div class="body">

          <Switch>
            <Route path={`${path}/login`} component={LoginPage}/>
            <Route path={`${path}/signup`} component={SignupPage}/>                  
            <Route component={NotFound}/>
          </Switch>
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

export { Accounts, LoginPage, SignupPage, NotFound };