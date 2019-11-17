import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const UserStatus = ({ isAuthenticated }) => {
  const [userDetails, setUserDetails] = useState({
    id: "",
    email: "",
    username: "",
    active: "",
    admin: ""
  });

  useEffect(() => {
    const options = {
      url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${window.localStorage.authToken}`
      }
    };
    axios(options)
      .then(res => {
        const data = res.data.data;
        setUserDetails({
          id: data.id,
          email: data.email,
          username: data.username,
          active: String(data.active),
          admin: String(data.admin)
        });
      })
      .catch(error => {
        console.log(error);
      });
  }, [setUserDetails]);

  if (!isAuthenticated) {
    return (
      <p>
        You must be logged in to view this. Click <Link to="/login">here</Link>{" "}
        to log back in.
      </p>
    );
  }
  return (
    <div>
      <ul>
        <li>
          <strong>User ID: </strong>
          {userDetails.id}
        </li>
        <li>
          <strong>Email: </strong>
          {userDetails.email}
        </li>
        <li>
          <strong>Username: </strong>
          {userDetails.username}
        </li>
        <li>
          <strong>Active: </strong>
          {userDetails.active}
        </li>
        <li>
          <strong>Admin: </strong>
          {userDetails.admin}
        </li>
      </ul>
    </div>
  );
};

export default UserStatus;
