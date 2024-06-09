import React from "react";
import { Navigate } from "react-router-dom";

function CheckCachedUser({ children, user, setUser, redirectTo }) {
  console.log("checking cached user");
  if (user !== null && user !== undefined && user.isAuth === true) {
    console.log("checking cached user1");

    return <Navigate to={redirectTo} />;
  } else if (
    (user === null || user === undefined) &&
    localStorage.getItem("user") !== null
  ) {
    const user = JSON.parse(localStorage.getItem("user"));
    console.log("checking cached user2");
    setUser(user);
  } else {
    return children;
  }
}

export default CheckCachedUser;
