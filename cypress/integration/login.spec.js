import { generate } from "randomstring";

const username = generate();
const email = `${username}@test.com`;

describe("Login", () => {
  it("should display the login form", () => {
    cy.visit("/login")
      .get("h1")
      .contains("Log In")
      .get("form");
  });

  it("should allow user to log in", () => {
    cy.visit("/register")
      .get("input[name='username']")
      .type(username)
      .get("input[name='email']")
      .type(email)
      .get("input[name='password']")
      .type("test")
      .get("input[type='submit']")
      .click();

    cy.get(".navbar-burger").click();
    cy.contains("Log Out").click();

    cy.get("a")
      .contains("Log In")
      .click()
      .get("input[name='email']")
      .type(email)
      .get("input[name='password']")
      .type("test")
      .get("input[type='submit']")
      .click()
      .wait(100);

    cy.contains("All Users");
    cy.contains(username);
    cy.get(".navbar-burger").click();
    cy.get(".navbar-menu").within(() => {
      cy.get(".navbar-item")
        .contains("User Status")
        .get(".navbar-item")
        .contains("Log Out")
        .get(".navbar-item")
        .contains("Log In")
        .should("not.be.visible")
        .get(".navbar-item")
        .contains("Register")
        .should("not.be.visible");
    });

    cy.get(".navbar-burger").click();
    cy.get("a")
      .contains("Log Out")
      .click();

    cy.get("p").contains("You are now logged out");
    cy.get(".navbar-menu").within(() => {
      cy.get(".navbar-item")
        .contains("User Status")
        .should("not.be.visible")
        .get(".navbar-item")
        .contains("Log Out")
        .should("not.be.visible")
        .get(".navbar-item")
        .contains("Log In")
        .get(".navbar-item")
        .contains("Register");
    });
  });
});
