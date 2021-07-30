import React from "react";
import { Cookies } from "react-cookie";
import Navbar from "../../components/Common/Navbar/Navbar";

const ScreenNotFound = () => {
  return (
    <div>
      <Navbar>xroads</Navbar>
      <div className="no-results">
        <h1>( ❛︵❛ )</h1>
        <h1 className="text">we couldn't find that page</h1>
      </div>
    </div>
  );
};
export default ScreenNotFound;
