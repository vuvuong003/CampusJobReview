import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Profile from "./../Pages/Profile";
import { BrowserRouter } from "react-router-dom";
import { protected_api_call } from "./../api/api";

// Mock the API call
jest.mock("../api/api", () => ({
  protected_api_call: jest.fn(),
}));

const mockProfileData = {
  username: "testuser",
  email: "testuser@example.com",
  first_name: "Test",
  last_name: "User",
  bio: "This is a test bio.",
};

describe("Profile Component", () => {
  beforeEach(() => {
    // Mock GET request for initial profile data
    protected_api_call.mockImplementation((url, data, method) => {
      if (method === "GET") {
        return Promise.resolve({
          ok: true,
          json: async () => mockProfileData,
        });
      }
      // Mock PUT request for profile update
      if (method === "PUT") {
        return Promise.resolve({
          ok: true,
          json: async () => ({ ...mockProfileData, ...data }),
        });
      }
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test("renders profile data", async () => {
    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByDisplayValue("testuser")).toBeInTheDocument();
      expect(
        screen.getByDisplayValue("testuser@example.com")
      ).toBeInTheDocument();
      expect(screen.getByDisplayValue("Test")).toBeInTheDocument();
      expect(screen.getByDisplayValue("User")).toBeInTheDocument();
      expect(
        screen.getByDisplayValue("This is a test bio.")
      ).toBeInTheDocument();
    });
  });

  test("updates profile data", async () => {
    render(
      <BrowserRouter>
        <Profile />
      </BrowserRouter>
    );

    // Wait for initial profile data to load
    await waitFor(() => {
      expect(screen.getByDisplayValue("testuser")).toBeInTheDocument();
    });

    // Update form fields
    const firstNameInput = screen.getByLabelText("First Name");
    const lastNameInput = screen.getByLabelText("Last Name");
    const bioInput = screen.getByLabelText("Bio");

    fireEvent.change(firstNameInput, { target: { value: "Updated" } });
    fireEvent.change(lastNameInput, { target: { value: "User" } });
    fireEvent.change(bioInput, { target: { value: "Updated bio." } });

    // Submit form
    fireEvent.click(screen.getByRole("button", { name: /Update Profile/i }));

    // Verify API call
    await waitFor(() => {
      expect(protected_api_call).toHaveBeenCalledWith(
        expect.stringContaining("auth/profile/"),
        expect.objectContaining({
          first_name: "Updated",
          last_name: "User",
          bio: "Updated bio.",
        }),
        "PUT"
      );
    });

    // Verify success message
    await waitFor(() => {
      expect(
        screen.getByText("Profile updated successfully.")
      ).toBeInTheDocument();
    });
  });
});
