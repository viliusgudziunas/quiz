import React from "react";
import { Link } from "react-router-dom";

const Navbar = ({ title }) => {
  return (
    <nav
      className="navbar is-dark"
      role="navigation"
      aria-label="main navigation"
    >
      <section className="container">
        <div className="navbar-brand">
          <strong className="navbar-item">{title}</strong>
          <span
            className="nav-toggle navbar-burger"
            onClick={() => {
              let toggle = document.querySelector(".nav-toggle");
              let menu = document.querySelector(".navbar-menu");
              toggle.classList.toggle("is-active");
              menu.classList.toggle("is-active");
            }}
          >
            <span />
            <span />
            <span />
          </span>
        </div>
        <div className="navbar-menu">
          <div className="navbar-start">
            <Link className="navbar-item" to="/">
              Home
            </Link>
            <Link className="navbar-item" to="/about">
              About
            </Link>
            <Link className="navbar-item" to="/status">
              User Status
            </Link>
          </div>
          <div className="navbar-end">
            <Link className="navbar-item" to="/register">
              Register
            </Link>
            <Link className="navbar-item" to="/login">
              Log In
            </Link>
            <Link className="navbar-item" to="/logout">
              Log Out
            </Link>
          </div>
        </div>
      </section>
    </nav>
  );
};

export default Navbar;
