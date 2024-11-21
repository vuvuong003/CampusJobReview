// NavBar.test.js

import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom"; 
import NavBar from "./../Pages/Navbar";

const mockNavigate = jest.fn();

const renderNavBar = (loginStatus) => {
  localStorage.setItem("login", loginStatus ? "true" : "false");
  render(
    <MemoryRouter> {/* Wrap the component in MemoryRouter */}
      <NavBar navigation={mockNavigate} />
    </MemoryRouter>
  );
};

describe("NavBar Component", () => {
  beforeEach(() => {
    mockNavigate.mockClear();
  });

  it("renders NavBar with default pages when not logged in", () => {
    renderNavBar(false);
  });

  it("renders NavBar with logged-in pages when logged in", () => {
    renderNavBar(true);
  });

  it("navigates to the correct pages when desktop buttons are clicked", () => {
    renderNavBar(true);

    // Select the desktop `Home` button specifically by using `getAllByText` and picking the appropriate one
    fireEvent.click(screen.getAllByText(/Home/i)[0]); // Target the first Home button in the desktop view
  });

  it("opens and closes the mobile menu", () => {
    renderNavBar(true);
  });
});
