import React, { useState } from "react";
import axios from "axios";

const AddUser = ({ setUserAdded }) => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");

  const addUser = e => {
    e.preventDefault();
    const data = { username, email };
    axios
      .post(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, data)
      .then(res => {
        setUserAdded(true);
        setUsername("");
        setEmail("");
      })
      .catch(err => {
        console.log(err.response.data);
      });
  };

  return (
    <form onSubmit={addUser}>
      <div className="field">
        <input
          type="text"
          className="input is-large"
          name="username"
          placeholder="Enter a username"
          required
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
      </div>
      <div className="field">
        <input
          type="email"
          className="input is-large"
          name="email"
          placeholder="Enter an email address"
          required
          value={email}
          onChange={e => setEmail(e.target.value)}
        />
      </div>
      <input
        type="submit"
        className="button is-primary is-large is-fullwidth"
        value="Submit"
      />
    </form>
  );
};

export default AddUser;
