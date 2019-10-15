import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import UsersList from "./components/UsersList";

const App = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        setUsers(res.data.data.users);
      })
      .catch(err => {
        console.log(err);
      });
  }, [setUsers]);

  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          <column className="is-one-third">
            <br />
            <h1 className="title is-1">All Users</h1>
            <hr />
            <br />
            <UsersList users={users} />
          </column>
        </div>
      </div>
    </section>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));
