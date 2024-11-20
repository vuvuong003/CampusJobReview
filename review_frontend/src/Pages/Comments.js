import React, { useState, useEffect, useCallback } from "react";
import { protected_api_call, comment_url } from "../api/api";
import { formatDistanceToNow } from "date-fns";

const Comments = ({ reviewId}) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  const fetchComments = useCallback(async () => {
    const response = await protected_api_call(`${comment_url}${reviewId}/`, {}, "GET");
    if (response.status === 200) {
      const data = await response.json();
      setComments(data);
    }
  }, [reviewId]);

  useEffect(() => {
    fetchComments();
  }, [fetchComments]);

  const handleAddComment = async () => {
    if (newComment.trim() === "") return;

    const response = await protected_api_call(
      `${comment_url}${reviewId}/`, { text: newComment }, "POST");
    if (response.status === 201) {
      const addedComment = await response.json();
      setComments([...comments, addedComment]);
      setNewComment("");
    }
  };

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
        {comments.map((comment) => (
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
            <button
              onClick={() => handleDeleteComment(comment.id)}
              className="text-red-500 hover:text-red-700"
              style={{
                marginLeft: "1rem", // Add space between the text and icon
                fontSize: "2rem", // Larger icon size
                alignSelf: "flex-start", // Align icon to the top
              }}
            >
              🗑️
            </button>
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
        >
          Post Comment
        </button>
      </div>
    </div>
  );
};

export default Comments;
