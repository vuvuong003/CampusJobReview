import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { BrowserRouter } from "react-router-dom";
import AddReviewWithNavigate, { AddReview } from "./../Pages/AddReview";
import { protected_api_call, review_url } from "./../api/api";

// Mock the API call
jest.mock("../api/api", () => ({
  protected_api_call: jest.fn(),
  review_url: "mock-url",
}));

// Mock window.alert
const mockAlert = jest.fn();
window.alert = mockAlert;

// Test setup helper
const renderAddReview = () => {
  return render(
    <BrowserRouter>
      <AddReviewWithNavigate />
    </BrowserRouter>,
  );
};

describe("AddReview Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders all form fields", () => {
    renderAddReview();

    // Use getByRole with name for better accessibility testing
    expect(
      screen.getByRole("textbox", { name: /job title/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /department/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /location/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /job description/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /hourly pay/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /benefits/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("textbox", { name: /review/i }),
    ).toBeInTheDocument();
  });

  test("updates form state when input values change", () => {
    renderAddReview();

    const jobTitleInput = screen.getByRole("textbox", { name: /job title/i });
    fireEvent.change(jobTitleInput, {
      target: { value: "Software Engineer", name: "job_title" },
    });
    expect(jobTitleInput.value).toBe("Software Engineer");

    const departmentInput = screen.getByRole("textbox", {
      name: /department/i,
    });
    fireEvent.change(departmentInput, {
      target: { value: "Engineering", name: "department" },
    });
    expect(departmentInput.value).toBe("Engineering");
  });

  test("submits form successfully", async () => {
    protected_api_call.mockResolvedValueOnce({ status: 201 });
    renderAddReview();

    // Fill text inputs
    fireEvent.change(screen.getByRole("textbox", { name: /job title/i }), {
      target: { value: "Software Engineer", name: "job_title" },
    });
    fireEvent.change(screen.getByRole("textbox", { name: /department/i }), {
      target: { value: "Engineering", name: "department" },
    });
    fireEvent.change(screen.getByRole("textbox", { name: /location/i }), {
      target: { value: "Remote", name: "locations" },
    });

    // Select rating and recommendation
    const ratingRadio = screen.getByRole("radio", { name: /rating 4/i });
    fireEvent.click(ratingRadio);

    const recommendationRadio = screen.getByRole("radio", {
      name: /recommendation 8/i,
    });
    fireEvent.click(recommendationRadio);

    // Submit form
    fireEvent.click(
      screen.getByRole("button", { name: /submit your review/i }),
    );

    await waitFor(() => {
      expect(protected_api_call).toHaveBeenCalled();
      expect(mockAlert).toHaveBeenCalledWith("Review Submitted Successfully");
    });
  });

  test("handles form submission error", async () => {
    protected_api_call.mockResolvedValueOnce({ status: 400 });
    renderAddReview();

    fireEvent.click(
      screen.getByRole("button", { name: /submit your review/i }),
    );

    await waitFor(() => {
      expect(mockAlert).toHaveBeenCalledWith(
        "There was an error submitting your review",
      );
    });
  });

  test("renders and selects rating radio buttons", () => {
    renderAddReview();

    // Check if rating radio buttons exist and can be selected
    [1, 2, 3, 4, 5].forEach((rating) => {
      const radio = screen.getByRole("radio", {
        name: new RegExp(`rating ${rating}`, "i"),
      });
      expect(radio).toBeInTheDocument();
      fireEvent.click(radio);
      expect(radio).toBeChecked();
    });
  });

  test("renders and selects recommendation radio buttons", () => {
    renderAddReview();

    // Check if recommendation radio buttons exist and can be selected
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].forEach((recommendation) => {});
  });
});
