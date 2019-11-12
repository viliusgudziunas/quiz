import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const UserStatus = ({ isAuthenticated }) => {
  const [email, setEmail] = useState("");
  const [id, setId] = useState("");
  const [username, setUsername] = useState("");

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
        setEmail(res.data.data.email);
        setId(res.data.data.id);
        setUsername(res.data.data.username);
      })
      .catch(error => {
        console.log(error);
      });
  }, [setEmail, setId, setUsername]);

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
          {id}
        </li>
        <li>
          <strong>Email: </strong>
          {email}
        </li>
        <li>
          <strong>Username: </strong>
          {username}
        </li>
      </ul>
    </div>
  );
};

export default UserStatus;
