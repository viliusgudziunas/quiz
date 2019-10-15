import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import UsersList from "./components/UsersList";
import AddUser from "./components/AddUser";

const App = () => {
  const [users, setUsers] = useState([]);

  const [userAdded, setUserAdded] = useState(false);
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        setUsers(res.data.data.users);
      })
      .catch(err => {
        console.log(err);
      });
    setUserAdded(false);
  }, [setUsers, userAdded]);

  return (
    <section className="section">
      <div className="container">
        <div className="columns">
          <div className="is-one-third">
            <br />
            <h1 className="title is-1">All Users</h1>
            <hr />
            <br />
            <AddUser setUserAdded={setUserAdded} />
            <hr />
            <br />
            <UsersList users={users} />
          </div>
        </div>
      </div>
    </section>
  );
};

ReactDOM.render(<App />, document.getElementById("root"));
