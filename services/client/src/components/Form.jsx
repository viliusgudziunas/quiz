import React, { useState, useEffect } from "react";
import axios from "axios";
import { Redirect } from "react-router-dom";

const Form = ({ formType, isAuthenticated, setIsAuthenticated }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const clearState = () => {
    setUsername("");
    setEmail("");
    setPassword("");
  };

  useEffect(() => {
    clearState();
  }, [formType]);

  const handleUserFormSubmit = e => {
    e.preventDefault();
    const data = { email, password };
    if (formType === "Register") {
      data.username = username;
    }
    axios
      .post(
        `${
          process.env.REACT_APP_USERS_SERVICE_URL
        }/auth/${formType.toLowerCase()}`,
        data
      )
      .then(res => {
        clearState();
        window.localStorage.setItem("authToken", res.data.auth_token);
        setIsAuthenticated(true);
      })
      .catch(err => {
        console.log(err.response.data);
      });
  };

  if (isAuthenticated) {
    return <Redirect to="/" />;
  }
  return (
    <div>
      {formType === "Login" && <h1 className="title is-1">Log In</h1>}
      {formType === "Register" && <h1 className="title is-1">Register</h1>}
      <hr />
      <br />
      <form onSubmit={handleUserFormSubmit}>
        {formType === "Register" && (
          <div className="field">
            <input
              type="text"
              className="input is-medium"
              name="username"
              placeholder="Enter a username"
              required
              value={username}
              onChange={e => setUsername(e.target.value)}
            />
          </div>
        )}
        <div className="field">
          <input
            type="email"
            className="input is-medium"
            name="email"
            placeholder="Enter an email address"
            required
            value={email}
            onChange={e => setEmail(e.target.value)}
          />
        </div>
        <div className="field">
          <input
            type="password"
            className="input is-medium"
            name="password"
            placeholder="Enter a password"
            required
            value={password}
            onChange={e => setPassword(e.target.value)}
          />
        </div>
        <input
          type="submit"
          className="button is-primary is-medium is-fullwidth"
          value="Submit"
        />
      </form>
    </div>
  );
};

export default Form;
