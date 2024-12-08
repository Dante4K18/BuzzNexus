import React, { useState } from "react";

function PostForm({ onPostCreated }) {
  const [content, setContent] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // Ensure content is not empty
    if (!content.trim()) {
      alert("Post content cannot be empty!");
      return;
    }

    // Send the new post to the backend
    fetch("/posts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content }),
    })
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
        throw new Error("Failed to create post");
      })
      .then((data) => {
        // Call the callback function to refresh the feed
        onPostCreated();
        setContent(""); // Clear the input
      })
      .catch((error) => {
        console.error(error);
        alert("An error occurred while creating the post.");
      });
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <textarea
        style={styles.textarea}
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="What's on your mind?"
        rows="4"
      />
      <button type="submit" style={styles.button}>
        Post
      </button>
    </form>
  );
}

const styles = {
  form: {
    margin: "20px auto",
    width: "90%",
    maxWidth: "500px",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  textarea: {
    width: "100%",
    padding: "10px",
    fontSize: "16px",
    border: "1px solid #ccc",
    borderRadius: "5px",
    marginBottom: "10px",
  },
  button: {
    backgroundColor: "#007bff",
    color: "#fff",
    padding: "10px 20px",
    fontSize: "16px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default PostForm;
