import React from "react";
import { BrowserRouter as Router, Route, Switch, Link } from "react-router-dom";


const ScreensHome = () => {  
  return (
    <div>
      This is the beginning. Maybe you should <Link to={"/login"}>Log In</Link>

      Or look at the Carousel Bug <Link to={"/carouselbug"}> Carousel Bug</Link>

    </div>
  );
};

export default ScreensHome;
