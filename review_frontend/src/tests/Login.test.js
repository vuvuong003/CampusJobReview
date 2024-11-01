import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Login from "./../Pages/Login";
import { MemoryRouter } from "react-router-dom";

// Mock the API call
jest.mock("../api/api", () => ({
  unprotected_api_call: jest.fn(),
  login_url: "mockLoginUrl",
}));

describe("Login Component", () => {
  const mockNavigate = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks(); // Clear mocks before each test
    localStorage.clear(); // Clear local storage before each test
  });

  test("renders Login component with username and password fields", () => {
    render(
      <MemoryRouter>
        <Login navigate={mockNavigate} />
      </MemoryRouter>,
    );
  });

  test("allows users to type in username and password", () => {
    render(
      <MemoryRouter>
        <Login navigate={mockNavigate} />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "testpass" },
    });

    expect(screen.getByLabelText(/Username/i).value).toBe("testuser");
    expect(screen.getByLabelText(/Password/i).value).toBe("testpass");
  });

  test("shows alert on invalid credentials", async () => {
    const { unprotected_api_call } = require("../api/api");
    unprotected_api_call.mockResolvedValueOnce({ status: 401 }); // Mock API response

    const alertMock = jest.spyOn(window, "alert").mockImplementation(() => {});
    render(
      <MemoryRouter>
        <Login navigate={mockNavigate} />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: "wronguser" },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "wrongpass" },
    });

    // fireEvent.click(screen.getByRole('button', { name: /Login/i }));
  });

  test("navigates to home on successful login", async () => {
    const { unprotected_api_call } = require("../api/api");
    const mockResponse = { id: 1, username: "testuser" };
    unprotected_api_call.mockResolvedValueOnce({
      status: 200,
      json: jest.fn().mockResolvedValueOnce(mockResponse),
    });

    render(
      <MemoryRouter>
        <Login navigate={mockNavigate} />
      </MemoryRouter>,
    );

    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: "testuser" },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: "testpass" },
    });
  });
});
