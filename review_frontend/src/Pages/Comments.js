/**
 * @fileoverview Display, insert and delete comments for job reviews
 * Contains components for displaying, inserting and deleting comments for each job review
 */
import React, { useState, useEffect, useCallback } from "react";
import { protected_api_call, comment_url } from "../api/api";
import { formatDistanceToNow } from "date-fns";

/**
 * Comments component that handles displaying, adding, and deleting comments for a review.
 * Fetches comments from the API, allows users to add new comments, and delete existing ones.
 * 
 * @param {Object} props - The props passed to the component.
 * @param {string} props.reviewId - The ID of the review for which comments are being managed.
 * @returns {JSX.Element} The rendered Comments component.
 */
const Comments = ({ reviewId, currentUser }) => {
  /**
   * State to hold the list of comments fetched from the API.
   * @type {Array}
   */
  const [comments, setComments] = useState([]);

  /**
   * State to hold a boolean indicating whether loadding spinner should be displayed or not.
   * @type {Boolean}
   */
  const [isLoadingSpinner, setIsLoadingSpinner] = useState(true);
  /**
   * State to hold the new comment text input by the user.
   * @type {string}
   */
  const [newComment, setNewComment] = useState("");

  /**
   * Fetches the list of comments for the current review ID from the API.
   * 
   * @async
   * @function
   */
  const fetchComments = useCallback(async () => {
    const response = await protected_api_call(`${comment_url}${reviewId}/`, {}, "GET");
    if (response && response.status === 200) {
      const data = await response.json();
      setComments(data);
      setIsLoadingSpinner(false);
    } else {
      alert("Failed to load comments");
      setIsLoadingSpinner(false);
    }

  }, [reviewId]);

  /**
   * Fetch comments when the component mounts or the review ID changes.
   */
  useEffect(() => {
    fetchComments();
  }, [fetchComments]);

  /**
   * Handles adding a new comment to the review.
   * Sends a POST request to the API and updates the state with the new comment.
   * 
   * @async
   * @function
   */
  const handleAddComment = async () => {
    if (newComment.trim() === "") return;

    const response = await protected_api_call(
      `${comment_url}${reviewId}/`, { text: newComment }, "POST");
    if (response.status === 201) {
      const addedComment = await response.json();
      setComments([...comments, addedComment]);
      setNewComment("");
    } else {
      alert("Failed to add comment");
    }
  };

  /**
   * Handles deleting a comment by its ID.
   * Sends a DELETE request to the API and refetches the comments if the deletion is successful.
   * 
   * @async
   * @function
   * @param {string} commentId - The ID of the comment to be deleted.
   */
  const handleDeleteComment = async (commentId) => {
    const response = await protected_api_call(
      `${comment_url}${reviewId}/${commentId}/`, {}, "DELETE");
    if (response.status === 204) {
      // Successfully deleted the comment, refetch the comments
      fetchComments();
    } else {
      alert("Failed to delete comment");
    }
  };

  return (
    <div className="comments-section mt-4">
      <h4 className="text-xl font-semibold mb-2">Comments</h4>
      <div className="comments-list">
        {isLoadingSpinner ?
          (<div className="flex justify-center items-center h-16">
            <div className="w-6 h-6 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" data-testid="loading_spinner"></div>
          </div>          
          )
          :
          comments.map((comment) => (
            <div
              key={comment.id}
              className="comment bg-gray-100 rounded-lg mb-2"
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                padding: "1rem",
              }}
            >
              {/* Comment text container */}
              <div
                className="comment-text"
                style={{
                  textAlign: "left", // Explicit left alignment
                  flex: 1, // Take up all available space
                }}
              >
                <p
                  className="text-sm text-gray-600"
                  style={{
                    margin: 0,
                    marginBottom: "0.5rem", // Consistent spacing between user and text
                  }}
                >
                  <strong>{comment.user}</strong> • {formatDistanceToNow(new Date(comment.created_at))} ago
                </p>
                <p
                  className="text-gray-800"
                  style={{
                    margin: 0,
                    whiteSpace: "pre-line", // Preserve formatting for multi-line comments
                  }}
                >
                  {comment.text}
                </p>
              </div>
              {/* Trash icon */}
              {
                (comment.user === currentUser) &&

                <button
                  type="submit"
                  onClick={() => handleDeleteComment(comment.id)}
                  className="text-red-500 hover:text-red-700"
                  style={{
                    marginLeft: "1rem",
                    fontSize: "2rem",
                    alignSelf: "flex-between",
                  }}
                  aria-label={`Delete comment`}
                >
                  🗑️
                </button>
              }

            </div>
          ))}
      </div>
      <div className="comment-input mb-4">
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Add a comment..."
          className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
        <button
          onClick={handleAddComment}
          className="bg-blue-500 text-white py-2 px-4 rounded-lg mt-2"
          aria-label="Post comment"
        >
          Post Comment
        </button>
      </div>
    </div>
  );
};

export default Comments;
