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
      screen.getByLabelText(/hourly pay/i),
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

    // Update rating slider
    const ratingSlider = screen.getByLabelText(/rating/i);
    fireEvent.change(ratingSlider, { target: { value: 4 } });
    expect(ratingSlider).toHaveValue("4");

    // Update recommendation slider
    const recommendationSlider = screen.getByLabelText(/recommendation/i);
    fireEvent.change(recommendationSlider, { target: { value: 8 } });
    expect(recommendationSlider).toHaveValue("8");

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

  test("renders and interacts with the Rating slider", () => {
    renderAddReview();
  
    // Get the slider using its accessible label
    const ratingSlider = screen.getByLabelText(/Rating/i);
  
    // Verify the slider is rendered
    expect(ratingSlider).toBeInTheDocument();
  
    // Simulate changing the slider value
    fireEvent.change(ratingSlider, { target: { value: 4 } });
  
    // Check if the slider's value is updated
    expect(ratingSlider).toHaveValue("4");
  
    // Verify the displayed recommendation value updates
    expect(screen.getByText("4")).toBeInTheDocument();
  });
  

  test("renders and interacts with the recommendation slider", () => {
    renderAddReview();
  
    // Get the slider using its accessible label
    const recommendationSlider = screen.getByLabelText(/Recommendation/i);
  
    // Verify the slider is rendered
    expect(recommendationSlider).toBeInTheDocument();
  
    // Simulate changing the slider value
    fireEvent.change(recommendationSlider, { target: { value: 7 } });
  
    // Check if the slider's value is updated
    expect(recommendationSlider).toHaveValue("7");
  
    // Verify the displayed recommendation value updates
    expect(screen.getByText("7")).toBeInTheDocument();
  });
  
});
