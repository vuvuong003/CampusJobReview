import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import { BrowserRouter } from "react-router-dom";
import Comments from "../Pages/Comments"; // Adjust the path as needed
import { protected_api_call, comment_url } from "../api/api";

// Mock the API call
jest.mock("../api/api", () => ({
  protected_api_call: jest.fn(),
  comment_url: "mock-comment-url",
}));

// Mock window.alert
const mockAlert = jest.fn();
window.alert = mockAlert;

// Test setup helper
const renderComments = (reviewId = 1, currentUser="User1") => {
  return render(
    <BrowserRouter>
      <Comments reviewId={reviewId} currentUser={currentUser}/>
    </BrowserRouter>
  );
};

describe("Comments Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("fail to fetch commets", async () => {
    renderComments();
  
    // Simulate an API failure (e.g., 500 Internal Server Error)
    protected_api_call.mockResolvedValueOnce({
      status: 500,
      json: jest.fn().mockResolvedValue({}),
    });
  
    // Wait for the error state to appear or handle it inside the component
    await waitFor(() => {
      expect(mockAlert).toHaveBeenCalledWith("Failed to load comments");
    });
  });

  test("fetch existing comments", async () => {
    renderComments();

    // Mock the API response
    const mockComments = [
      { id: 1, user: "User1", text: "Great review!", created_at: new Date().toISOString() },
      { id: 2, user: "User2", text: "I agree with the points.", created_at: new Date().toISOString() },
    ];

    // Log the mock setup to confirm it's being applied correctly
    protected_api_call.mockResolvedValueOnce({
      status: 200,
      json: jest.fn().mockResolvedValue(mockComments),
    });
    
    // Wait for the component to update with comments
    await waitFor(() => {
        expect(
            screen.getByRole("textbox", { text: /Great review!/i }),
        ).toBeInTheDocument();
        expect(
            screen.getByRole("textbox", { text: /I agree with the points./i }),
        ).toBeInTheDocument();
    });
  });

  test("successfully add a new comment", async () => {
    // Mock the API responses for posting a comment
    const mockNewComment = {
      id: 2,
      user: "User2",
      text: "This is a new comment.",
      created_at: new Date().toISOString(),
    };

    protected_api_call
      .mockResolvedValueOnce({
        status: 200,
        json: jest.fn().mockResolvedValueOnce([
          {
            id: 1,
            user: "User1",
            text: "Existing comment.",
            created_at: new Date().toISOString(),
          },
        ]), // initial comments
      })
      .mockResolvedValueOnce({
        status: 201,
        json: jest.fn().mockResolvedValueOnce(mockNewComment),
      });

    render(<Comments reviewId={1} />);

    // Simulate adding a comment
    fireEvent.change(screen.getByPlaceholderText("Add a comment..."), {
      target: { value: "This is a new comment." },
    });
    fireEvent.click(screen.getByText("Post Comment"));

    // Check if the new comment was added to the list
    await waitFor(() => {
        expect(
            screen.getByRole("textbox", { text: /This is a new comment./i }),
        ).toBeInTheDocument();
    });
  });

  test("successfully delete a comment", async () => {
    renderComments();
    const mockComments = [
        {
          id: 1,
          user: "User1",
          text: "Great review!",
          created_at: new Date().toISOString(),
        },
      ];
    protected_api_call.mockResolvedValueOnce({ status: 200, json: jest.fn().mockResolvedValueOnce(mockComments) });

    // The comment is located
    expect(
        screen.getByRole("textbox", { text: /Great review!/i }),
    ).toBeInTheDocument();

    fireEvent.click(
        screen.getByRole("button", { "aria-label": /Delete comment/i }),
    );

    // After deletion, we expect the comment to be removed
    await waitFor(() => {
        expect(screen.queryByText(/Great review!/i)).not.toBeInTheDocument();
    });
  });

  test("fail to add a comment", async () => {
    const mockComments = [
        {
          id: 1,
          user: "User1",
          text: "This comment will fail to add.",
          created_at: new Date().toISOString(),
        },
      ];
  
    protected_api_call.mockResolvedValueOnce({
      status: 200,
      json: jest.fn().mockResolvedValueOnce(mockComments),
    });
  
    renderComments();
  
    // Simulate a failed POST response
    protected_api_call.mockResolvedValueOnce({
      status: 500,
      json: jest.fn().mockResolvedValueOnce({}),
    });
    
    fireEvent.change(screen.getByPlaceholderText("Add a comment..."), {
        target: { value: "This is a failed comment." },
    });
    fireEvent.click(screen.getByRole("button", { name: /Post comment/i }));
      
    await waitFor(() => {
      expect(mockAlert).toHaveBeenCalledWith("Failed to add comment");
    });
  });

  test("fail to delete a comment", async () => {
    const mockComments = [
      {
        id: 1,
        user: "User1",
        text: "This comment will fail to delete.",
        created_at: new Date().toISOString(),
      },
    ];
  
    // Mock the GET response for fetching comments
    protected_api_call.mockResolvedValueOnce({
      status: 200,
      json: jest.fn().mockResolvedValueOnce(mockComments),
    });
  
    renderComments();
  
    // Wait for the comments to be rendered
    await waitFor(() => {
      expect(screen.getByText(/This comment will fail to delete./i)).toBeInTheDocument();
    });
  
    // Mock the DELETE response to simulate a failure
    protected_api_call.mockResolvedValueOnce({
      status: 500,
      json: jest.fn().mockResolvedValueOnce({}),
    });
  
    // Trigger the delete action
    fireEvent.click(screen.getByRole("button", { name: /Delete comment/i }));
  
    // Assert the failure alert
    await waitFor(() => {
      expect(mockAlert).toHaveBeenCalledWith("Failed to delete comment");
    });
  });  
  
});
