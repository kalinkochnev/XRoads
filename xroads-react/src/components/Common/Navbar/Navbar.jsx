import React from "react";
import "./Navbar.scss";

class Navbar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: null,
    };
  }

  render() {
    return (
      <div class="navbar-simple">
        <div class="xroadsLogo">
          <img class="logo-svg" src={require('../icons/logo-color.svg')}></img>
        </div>
        <div className="navbar-buttons">
          <button>logout</button>
        </div>
      </div>
    );
  }
}

export default Navbar;
