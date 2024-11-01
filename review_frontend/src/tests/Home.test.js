import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Home from "./../Pages/Home";
import { MemoryRouter } from "react-router-dom";

describe("Home Component", () => {
  beforeEach(() => {
    localStorage.clear(); // Clear local storage before each test
  });

  test("renders Home component with title and buttons", () => {
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>,
    );

    const title = screen.getByText(/NC State Campus Jobs/i);
    const addButton = screen.getByRole("button", { name: /Add Reviews/i });
    const viewButton = screen.getByRole("button", { name: /View Reviews/i });

    expect(title).toBeInTheDocument();
    expect(addButton).toBeInTheDocument();
    expect(viewButton).toBeInTheDocument();
  });

  test("shows alert when adding review without login", () => {
    const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {});
    const navigate = jest.fn();
    render(
      <MemoryRouter>
        <Home navigate={navigate} />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole("button", { name: /Add Reviews/i }));

    expect(alertMock).toHaveBeenCalledWith("Please login to add reviews");
    expect(navigate).not.toHaveBeenCalled();

    alertMock.mockRestore(); // Restore alert
  });

  test("navigates to view-reviews when logged in and view reviews button is clicked", () => {
    localStorage.setItem("login", "true");

    const navigate = jest.fn();
    render(
      <MemoryRouter>
        <Home navigate={navigate} />
      </MemoryRouter>,
    );

    // Use screen.getAllByRole to find all buttons and then select the correct one
    const viewButtons = screen.getAllByRole("button", {
      name: /View Reviews/i,
    });
    fireEvent.click(viewButtons[0]); // Click the first one if multiple are found
  });

  test("shows alert when viewing reviews without login", () => {
    const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {});
    const navigate = jest.fn();
    render(
      <MemoryRouter>
        <Home navigate={navigate} />
      </MemoryRouter>,
    );

    fireEvent.click(screen.getByRole("button", { name: /View Reviews/i }));

    expect(alertMock).toHaveBeenCalledWith("Please login to view reviews");
    expect(navigate).not.toHaveBeenCalled();

    alertMock.mockRestore(); // Restore alert
  });
});
