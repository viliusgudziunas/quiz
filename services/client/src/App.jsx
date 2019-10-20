import React, { useState, useEffect } from "react";
import axios from "axios";
import { Route, Switch } from "react-router-dom";
import UsersList from "./components/UsersList";
import AddUser from "./components/AddUser";
import About from "./components/About";
import NavBar from "./components/NavBar";
import Form from "./components/Form";

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

  const [title, setTitle] = useState("TestDrivenTutorial.io");

  return (
    <div>
      <NavBar title={title} />
      <section className="section">
        <div className="container">
          <div className="columns">
            <div className="is-half">
              <br />
              <Switch>
                <Route
                  exact
                  path="/"
                  render={() => (
                    <div>
                      <h1 className="title is-1">All Users</h1>
                      <hr />
                      <br />
                      <AddUser setUserAdded={setUserAdded} />
                      <hr />
                      <br />
                      <UsersList users={users} />
                    </div>
                  )}
                />
                <Route exact path="/about" component={About} />
                <Route
                  exact
                  path="/register"
                  render={() => <Form formType={"Register"} />}
                />
                <Route
                  exact
                  path="/login"
                  render={() => <Form formType={"Login"} />}
                />
              </Switch>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default App;
