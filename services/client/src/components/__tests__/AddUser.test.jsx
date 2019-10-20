import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";
import AddUser from "../AddUser";

test("AddUser renders properly", () => {
  const wrapper = shallow(<AddUser />);
  const element = wrapper.find("form");
  expect(element.find("input").length).toBe(3);

  const usernameField = element.find("input").get(0);
  expect(usernameField.props.name).toBe("username");
  expect(usernameField.props.value).toBe("");

  const emailField = element.find("input").get(1);
  expect(emailField.props.name).toBe("email");
  expect(emailField.props.value).toBe("");

  const submitButton = element.find("input").get(2);
  expect(submitButton.props.type).toBe("submit");
  expect(submitButton.props.value).toBe("Submit");
});

test("AddUser renders a snapshot properly", () => {
  const tree = renderer.create(<AddUser />).toJSON();
  expect(tree).toMatchSnapshot();
});
