import React from 'react';
import { Navbar } from './ClubPage'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './styles/_accountForm.scss';
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
        <div id="body">

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
      <div class="accountLayout">
        <form class="accountForm">
          <div class="fields">
            <input class="first-field" type="email" name="email-address" placeholder="Email Address"/>
            <input class="last-field" type="password" name="password" placeholder="Password"/>
          </div>
          
          <input id="account-submit" type="submit" value="Login"/>
        </form>
      </div>
    );
  }
}

// TODO break up the signup page into several parts for better user experience
class SignupPage extends React.Component {

  render() {
    return (
      <div class="accountLayout">
        <form class="accountForm">
          <div class="fields">
            <input class="first-field" type="email" name="email-address" placeholder="Email Address"/>
            <input type="tel" name="phone-number" pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}" placeholder="Phone number"/>
            <input type="text" name="first-name" placeholder="First name"/>
            <input type="text" name="last-name" placeholder="Last name"/>
            <input type="password" name="password" placeholder="Password"/>
            <input class="last-field" type="password" name="password" placeholder="Confirm Password"/>
          </div>
          <input id="account-submit" type="submit" value="sign up"/>
        </form>
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