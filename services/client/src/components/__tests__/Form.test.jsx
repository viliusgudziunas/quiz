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
  {
    formType: "Login",
    title: "Log In",
    formFields: ["email", "password"]
  }
];

describe("Form", () => {
  testData.forEach(el => {
    const component = <Form {...el} />;
    it("should match the snapshot", () => {
      const tree = renderer.create(component).toJSON();
      expect(tree).toMatchSnapshot();
    });

    const wrapper = shallow(component);
    if (el.formType === "Register") {
      it("should have three input fields", () => {
        expect(wrapper.find(".field").length).toBe(el.formFields.length);
      });

      it("should have an username field", () => {
        expect(wrapper.find("input[name='username']").length).toEqual(1);
      });
    } else if (el.formType == "Login") {
      it("should have two input fields", () => {
        expect(wrapper.find(".field").length).toBe(el.formFields.length);
      });
    }

    it("should have an email field", () => {
      expect(wrapper.find("input[name='email']").length).toEqual(1);
    });

    it("should have a password field", () => {
      expect(wrapper.find("input[name='password']").length).toEqual(1);
    });
  });
});

describe("When not authenticated", () => {
  testData.forEach(el => {
    const component = <Form {...el} />;
    it(`${el.formType} Form renders properly`, () => {
      const wrapper = shallow(component);
      const h1 = wrapper.find("h1");
      expect(h1.length).toBe(1);
      expect(h1.get(0).props.children).toBe(el.title);

      const formGroup = wrapper.find(".field");
      expect(formGroup.length).toBe(el.formFields.length);
      formGroup.forEach((field, index) => {
        expect(field.get(0).props.children.props.name).toBe(
          el.formFields[index]
        );
        expect(field.get(0).props.children.props.value).toBe("");
      });

      const submitButton = wrapper.find(".button").get(0);
      expect(submitButton.props.type).toBe("submit");
      expect(submitButton.props.value).toBe("Submit");
    });
  });
});

describe("When authenticated", () => {
  testData.forEach(el => {
    const component = <Form formType={el.formType} isAuthenticated={true} />;
    it(`${el.formType} redirects properly`, () => {
      const wrapper = shallow(component);
      expect(wrapper.find("Redirect")).toHaveLength(1);
    });
  });
});
