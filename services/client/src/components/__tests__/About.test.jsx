import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";
import About from "../About";

describe("About component", () => {
  it("should match the snapshot", () => {
    const tree = renderer.create(<About />).toJSON();
    expect(tree).toMatchSnapshot();
  });

  const wrapper = shallow(<About />);
  it("should have a title", () => {
    const element = wrapper.find("h1");
    expect(element.length).toBe(1);
    expect(element.get(0).props.className).toBe("title is-1");
    expect(element.get(0).props.children).toBe("About");
  });

  it("should have a paragraph", () => {
    const element = wrapper.find("p");
    expect(element.length).toBe(1);
    expect(element.get(0).props.children).toBe("Add something relevant here");
  });
});
