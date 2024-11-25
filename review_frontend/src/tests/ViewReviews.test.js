import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { BrowserRouter } from "react-router-dom";
import ReviewsWithNavigate from "../Pages/ViewReviews";
import { unprotected_api_call, protected_api_call } from "../api/api";

// Mock the API call
jest.mock("../api/api", () => ({
    unprotected_api_call: jest.fn(),
    all_reviews_url: "mock_reviews_url",
    protected_api_call: jest.fn(),
    comment_url: 'mock_comment_url',
}));

// Mock window.alert
const mockAlert = jest.fn();
window.alert = mockAlert;

// Test setup helper
const renderViewReviews = () => {
    return render(
        <BrowserRouter>
            <ReviewsWithNavigate />
        </BrowserRouter>,
    );
};

describe("ViewReview Component", () => {
    const mockJobReviews = [
        {
          id: 1,
          job_title: "Software Engineer",
          job_description: "Develop software applications.",
          department: "IT",
          locations: "Raleigh",
          hourly_pay: 50,
          benefits: "Health insurance",
          review: "Great place to work.",
          rating: 2,
          recommendation: 100,
          reviewed_by: "Alice",
        },
        {
          id: 2,
          job_title: "Data Scientist",
          job_description: "Analyze data for insights.",
          department: "Analytics",
          locations: "Durham",
          hourly_pay: 45,
          benefits: "401k",
          review: "Good learning experience.",
          rating: 1,
          recommendation: 80,
          reviewed_by: "Bob",
        },
        {
          id: 3,
          job_title: "Product Manager",
          job_description: "Lead product development efforts.",
          department: "Product",
          locations: "Chapel Hill",
          hourly_pay: 55,
          benefits: "Stock options, Health insurance",
          review: "Challenging but rewarding role.",
          rating: 4,
          recommendation: 90,
          reviewed_by: "Charlie",
        },
        {
          id: 4,
          job_title: "UX Designer",
          job_description: "Design user interfaces and improve user experience.",
          department: "Design",
          locations: "Raleigh",
          hourly_pay: 50,
          benefits: "Health insurance, Gym membership",
          review: "Creative and collaborative team environment.",
          rating: 5,
          recommendation: 95,
          reviewed_by: "Dana",
        },
      ];
      

    const checkFiltersRendered = () => {
        expect(screen.getByPlaceholderText("Department")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Location")).toBeInTheDocument();
        expect(screen.getByPlaceholderText("Job Title")).toBeInTheDocument();
        expect(screen.getByRole("combobox", { name: "Min Rating" })).toBeInTheDocument();
        expect(screen.getByRole("combobox", { name: "Max Rating" })).toBeInTheDocument();
    }


    beforeEach(() => {
        jest.clearAllMocks();

        unprotected_api_call.mockResolvedValueOnce({
            status: 200,
            json: async () => mockJobReviews,
        });

        protected_api_call.mockResolvedValueOnce({
            status: 200,
            json: async () => [
                { id: '1', user: 'User1', text: 'This is comment 1', created_at: '2024-11-01T00:00:00Z' },
                { id: '2', user: 'User2', text: 'This is comment 2', created_at: '2024-11-02T00:00:00Z' },
            ],
        })
    });

    test("Renders all the job reviews", async () => {
        renderViewReviews();

        // check if the navbar is rendered
        expect(screen.getByTestId("AppBar")).toBeInTheDocument();

        // check if all the filters are rendered
        checkFiltersRendered();

        // checking if all the job reviews are displayed
        const jobTitles = await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);
        expect(jobTitles).toHaveLength(mockJobReviews.length);
    });

    test("Expands and collapses job reviews", async () => {
        renderViewReviews();

        // Wait for job rows
        const expandButtons = await screen.findAllByText("▼");
        expect(expandButtons).toHaveLength(mockJobReviews.length);

        // making sure that the expanded review is not visible before expanding the job review
        let expandedReview = screen.queryByText("Great place to work.");
        expect(expandedReview).not.toBeInTheDocument();
        // Expand the first review
        fireEvent.click(expandButtons[0]);

        // Wait for the review to appear after expansion
        expandedReview = await screen.findByText("Great place to work.");
        expect(expandedReview).toBeInTheDocument();

        // verify all the comments are displayed
        expect(await screen.findByText('This is comment 1')).toBeInTheDocument();
        expect(await screen.findByText('This is comment 2')).toBeInTheDocument();

        // Collapse the review
        const collapseButton = screen.getByText("▲");
        fireEvent.click(collapseButton);

        // Wait for the review to be removed after collapsing
        const collapsedReview = screen.queryByText("Great place to work.");
        expect(collapsedReview).not.toBeInTheDocument();
    });

    test("Filters reviews based on department", async () => {
        renderViewReviews();

        // Wait for the job reviews to appear
        await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);

        const departmentInput = screen.getByPlaceholderText("Department");
        fireEvent.change(departmentInput, { target: { value: "IT" } });

        // Apply filter
        fireEvent.click(screen.getByText("Filter"));

        // Check the filtered result
        expect(screen.queryByText(/Software Engineer/i)).toBeInTheDocument();
        expect(screen.queryByText(/Data Scientist/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/Product Manager/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/UX Designer/i)).not.toBeInTheDocument();
    });

    test("Filters reviews based on location", async () => {
        renderViewReviews();

        // Wait for the job reviews to appear
        await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);

        const locationInput = screen.getByPlaceholderText("Location");
        fireEvent.change(locationInput, { target: { value: "Raleigh" } });

        fireEvent.click(screen.getByText("Filter"));

        // Check the filtered result
        expect(screen.queryByText(/Software Engineer/i)).toBeInTheDocument();
        expect(screen.queryByText(/Data Scientist/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/Product Manager/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/UX Designer/i)).toBeInTheDocument();
    });

    test("Filters reviews based on title", async () => {
        renderViewReviews();
        // Wait for the job reviews to appear
        await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);

        const jobTitleInput = screen.getByPlaceholderText("Job Title");
        fireEvent.change(jobTitleInput, { target: { value: "Mana" } });

        fireEvent.click(screen.getByText("Filter"));

        // Check the filtered result (should contain jobs with job titles containing 'mana')
        expect(screen.queryByText(/Software Engineer/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/Data Scientist/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/Product Manager/i)).toBeInTheDocument();
        expect(screen.queryByText(/UX Designer/i)).not.toBeInTheDocument();
    });

    test("Filters reviews based on minimum rating", async () => {
        renderViewReviews();

        await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);

        // Select 3 as the minimum rating the drop down menu
        fireEvent.change(screen.getByLabelText('Min Rating'), {
            target: { value: 3 },
        })

        // click on the filter button
        fireEvent.click(screen.getByText("Filter"));

        expect(screen.queryByText(/Software Engineer/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/Data Scientist/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/Product Manager/i)).toBeInTheDocument();
        expect(screen.queryByText(/UX Designer/i)).toBeInTheDocument();
    });

    test("Filters reviews based on maximum rating", async () => {
        renderViewReviews();

        await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);

        // select 3 as the maximum rating in the drop down menu
        fireEvent.change(screen.getByLabelText('Max Rating'), {
            target: { value: 3 },
        })

        // click on the filter button
        fireEvent.click(screen.getByText("Filter"));

        expect(screen.queryByText(/Software Engineer/i)).toBeInTheDocument();
        expect(screen.queryByText(/Data Scientist/i)).toBeInTheDocument();
        expect(screen.queryByText(/Product Manager/i)).not.toBeInTheDocument();
        expect(screen.queryByText(/UX Designer/i)).not.toBeInTheDocument();
    });

    test("Resets the filters", async () => {
        renderViewReviews();

        // wait for all the job reviews to render
        await screen.findAllByText(/Software Engineer|Data Scientist|Product Manager|UX Designer/);

        // apply few filters
        const locationInput = screen.getByPlaceholderText("Location");
        fireEvent.change(locationInput, { target: { value: "Raleigh" } });

        fireEvent.change(screen.getByLabelText('Min Rating'), {
            target: { value: 3 },
        });

         // click on the filter button
         fireEvent.click(screen.getByText("Filter"));

         // check the filtered list
         expect(screen.queryByText(/Software Engineer/i)).not.toBeInTheDocument();
         expect(screen.queryByText(/Data Scientist/i)).not.toBeInTheDocument();
         expect(screen.queryByText(/Product Manager/i)).not.toBeInTheDocument();
         expect(screen.queryByText(/UX Designer/i)).toBeInTheDocument();

         // click on the reset button
         fireEvent.click(screen.getByText("Reset"));

         // check if all the job reviews are rendered again
         expect(screen.queryByText(/Software Engineer/i)).toBeInTheDocument();
         expect(screen.queryByText(/Data Scientist/i)).toBeInTheDocument();
         expect(screen.queryByText(/Product Manager/i)).toBeInTheDocument();
         expect(screen.queryByText(/UX Designer/i)).toBeInTheDocument();
    })
});
