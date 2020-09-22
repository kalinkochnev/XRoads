import React from "react";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";


const ScreensHome = () => {  
  return (
    <div>
      This is the beginning. Maybe you should <Link to={"/login"}>Log In</Link>

    </div>
  );
};

export default ScreensHome;
