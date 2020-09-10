import React from "react";
import { Cookies } from "react-cookie";


const ScreenNotFound = () => {
  console.log(new Cookies().getAll(['yo', 'blah']))
  return (
    <div>
      <h1>this page was not found </h1>
    </div>
  );
};
export default ScreenNotFound;
