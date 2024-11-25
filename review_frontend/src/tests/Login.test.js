import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import Login from "./../Pages/Login";
import ForgotPassword from "../Pages/ForgotPassword";

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

    const alertMock = jest.spyOn(window, "alert").mockImplementation(() => { });
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

  test('clicking on Forgot password redirects to /forgot-password and renders the ForgotPassword page', async () => {
    const { unprotected_api_call } = require("../api/api");

    unprotected_api_call.mockResolvedValueOnce({
      status: 200, 
      ok: true
    })
    
    // Render the component wrapped in a MemoryRouter
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Routes>
      </MemoryRouter>
    );

    // Find the "Forgot password?" link
    const forgotPasswordLink = screen.getByRole('link', { name: /Forgot Password\?/i });

    expect(forgotPasswordLink).toBeInTheDocument();

    // Simulate a click event on the link
    fireEvent.click(forgotPasswordLink);

    // Check if the ForgotPassword page content is rendered
    const enterEmailInput = screen.getByPlaceholderText(/Enter Email/i);
    expect(enterEmailInput).toBeInTheDocument();

    // checking if the "Send OTP" button exists
    let button = screen.getByText("Send OTP");
    expect(button).toBeInTheDocument();

    // clicking the button
    fireEvent.click(button);

    const loadingSpinner = screen.getByTestId("loading_spinner");
    expect(loadingSpinner).toBeInTheDocument();

    // wait for the otp text to appear
    const otpText = await screen.findByText("A one-time password has been sent to your email id.");
    expect(otpText).toBeInTheDocument();

    // loading spinner should disappear
    expect(loadingSpinner).not.toBeInTheDocument();

    // enter otp input should appear
    const enterOTP = screen.getByPlaceholderText("Enter one-time password");
    expect(enterOTP).toBeInTheDocument();

    // the button's text should be changed
    button = screen.getByText("Submit");
    expect(button).toBeInTheDocument();
  });

  test('clicking on Forgot password redirects to /forgot-password and entered email does not exist', async () => {
    const { unprotected_api_call } = require("../api/api");

    unprotected_api_call.mockResolvedValueOnce({
      ok: false,
      status: 400,
    })
    
    // Render the component wrapped in a MemoryRouter
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Routes>
      </MemoryRouter>
    );

    // Find the "Forgot password?" link
    const forgotPasswordLink = screen.getByRole('link', { name: /Forgot Password\?/i });

    expect(forgotPasswordLink).toBeInTheDocument();

    // Simulate a click event on the link
    fireEvent.click(forgotPasswordLink);

    // Check if the ForgotPassword page content is rendered
    const enterEmailInput = screen.getByPlaceholderText(/Enter Email/i);
    expect(enterEmailInput).toBeInTheDocument();

    // checking if the "Send OTP" button exists
    let button = screen.getByText("Send OTP");
    expect(button).toBeInTheDocument();

    // clicking the button
    fireEvent.click(button);

    // check if bad request alert is displayed
    await waitFor(() => expect(window.alert).toHaveBeenCalledWith("Bad request! The entered email id does not exist."));
  });

  test('clicking on Forgot password redirects to /forgot-password and entered OTP does not match', async () => {
    const { unprotected_api_call } = require("../api/api");

    unprotected_api_call.mockResolvedValueOnce({
      ok: true,
      status: 200,
    })
    
    // Render the component wrapped in a MemoryRouter
    render(
      <MemoryRouter initialEntries={['/login']}>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/forgot-password" element={<ForgotPassword />} />
        </Routes>
      </MemoryRouter>
    );

    // Find the "Forgot password?" link
    const forgotPasswordLink = screen.getByRole('link', { name: /Forgot Password\?/i });

    expect(forgotPasswordLink).toBeInTheDocument();

    // Simulate a click event on the link
    fireEvent.click(forgotPasswordLink);

    // Check if the ForgotPassword page content is rendered
    const enterEmailInput = screen.getByPlaceholderText(/Enter Email/i);
    expect(enterEmailInput).toBeInTheDocument();

    // checking if the "Send OTP" button exists
    let button = screen.getByText("Send OTP");
    expect(button).toBeInTheDocument();

    // clicking the button
    fireEvent.click(button);

    // enter otp input should appear
    const enterOTP = await screen.findByPlaceholderText("Enter one-time password");
    expect(enterOTP).toBeInTheDocument();

    fireEvent.change(enterOTP, { target: { value: "mock_otp"}});

    button = screen.getByText("Submit");
    fireEvent.click(button);

    // check if bad request alert is displayed
    await waitFor(() => expect(window.alert).toHaveBeenCalledWith("OTP entered is not valid. Try again."));
  });
});
