import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";
import AddUser from "../AddUser";

test("AddUser renders properly", () => {
  const wrapper = shallow(<AddUser />);
  const element = wrapper.find("form");
  expect(element.find("input").length).toBe(3);

  const username_field = element.find("input").get(0);
  expect(username_field.props.name).toBe("username");
  expect(username_field.props.value).toBe("");

  const email_field = element.find("input").get(1);
  expect(email_field.props.name).toBe("email");
  expect(email_field.props.value).toBe("");

  const submit_button = element.find("input").get(2);
  expect(submit_button.props.type).toBe("submit");
  expect(submit_button.props.value).toBe("Submit");
});

test("AddUser renders a snapshot properly", () => {
  const tree = renderer.create(<AddUser />).toJSON();
  expect(tree).toMatchSnapshot();
});
