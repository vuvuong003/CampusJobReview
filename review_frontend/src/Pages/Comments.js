import React, { useState, useEffect } from "react";
import { protected_api_call, comment_url } from "../api/api";
import { formatDistanceToNow } from "date-fns";

const Comments = ({ reviewId}) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    const fetchComments = async () => {
      const response = await protected_api_call(`${comment_url}${reviewId}/`, {}, "GET");
      if (response.status === 200) {
        const data = await response.json();
        setComments(data);
      }
    };
    fetchComments();
  }, [reviewId]);

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

  return (
    <div className="comments-section mt-4">
      <h4 className="text-xl font-semibold mb-2">Comments</h4>
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
      <div className="comments-list">
        {comments.map((comment) => (
          <div key={comment.commentId} className="comment bg-gray-100 p-4 rounded-lg mb-2">
            <p className="text-sm text-gray-600">
              <strong>{comment.user}</strong> • {formatDistanceToNow(new Date(comment.created_at))} ago
            </p>
            <p>{comment.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Comments;
