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
      <div className="navbar-simple">
        <div className="xroadsLogo">
          <h1>xroads</h1>
        </div>
        <div className="navbar-buttons">
          <button>logout</button>
        </div>
      </div>
    );
  }
}

export default Navbar;
