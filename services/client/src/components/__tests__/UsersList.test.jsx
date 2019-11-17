import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";
import UsersList from "../UsersList";

describe("UsersList component", () => {
  it("should match the snapshot", () => {
    const tree = renderer.create(<UsersList />).toJSON();
    expect(tree).toMatchSnapshot();
  });

  const wrapper = shallow(<UsersList />);
  it("should have a title", () => {
    const element = wrapper.find("h1");
    expect(element.length).toBe(1);
    expect(element.get(0).props.className).toBe("title is-1");
    expect(element.get(0).props.children).toBe("All Users");
  });

  it("should have a table", () => {
    const table = wrapper.find("table");
    expect(table.length).toBe(1);

    expect(wrapper.find("thead").length).toBe(1);
    const th = wrapper.find("th");
    expect(th.length).toBe(5);
    expect(th.get(0).props.children).toBe("ID");
    expect(th.get(1).props.children).toBe("Email");
    expect(th.get(2).props.children).toBe("Username");
    expect(th.get(3).props.children).toBe("Active");
    expect(th.get(4).props.children).toBe("Admin");

    expect(wrapper.find("tbody").length).toBe(1);
    expect(wrapper.find("tbogy > tr").length).toBe(0);
  });
});
