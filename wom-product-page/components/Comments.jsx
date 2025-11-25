import { useState } from "react";

export default function Comments() {
  const [comments, setComments] = useState(["Great product!"]);

  const addComment = () => {
    const newComment = document.getElementById("comment").value;
    setComments([...comments, newComment]);
    document.getElementById("comment").value = "";
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h2 className="text-xl font-bold mb-3">Customer Comments</h2>
      <textarea
        id="comment"
        className="w-full border p-2 rounded-lg"
        placeholder="Write your comment..."
      ></textarea>
      <button
        onClick={addComment}
        className="mt-2 px-4 py-2 bg-black text-white rounded-lg"
      >
        Post Comment
      </button>

      <ul className="mt-4 space-y-2">
        {comments.map((c, i) => (
          <li key={i} className="border p-2 rounded-lg">{c}</li>
        ))}
      </ul>
    </div>
  );
}
