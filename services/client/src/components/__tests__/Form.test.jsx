import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";
import Form from "../Form";

const testData = [
  {
    formType: "Register",
    title: "Register",
    formFields: ["username", "email", "password"]
  },
  { formType: "Login", title: "Log In", formFields: ["email", "password"] }
];

testData.forEach(el => {
  test(`${el.formType} Form renders properly`, () => {
    const component = <Form formType={el.formType} />;
    const wrapper = shallow(component);
    const h1 = wrapper.find("h1");
    expect(h1.length).toBe(1);
    expect(h1.get(0).props.children).toBe(el.title);

    const formGroup = wrapper.find(".field");
    expect(formGroup.length).toBe(el.formFields.length);
    formGroup.forEach((field, index) => {
      expect(field.get(0).props.children.props.name).toBe(el.formFields[index]);
      expect(field.get(0).props.children.props.value).toBe("");
    });

    const submitButton = wrapper.find(".button").get(0);
    expect(submitButton.props.type).toBe("submit");
    expect(submitButton.props.value).toBe("Submit");
  });

  test(`${el.formType} Form renders a snpashot properly`, () => {
    const component = <Form formType={el.formType} />;
    const tree = renderer.create(component).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
