import React, { useState, useEffect } from "react";

function Profile({ userId }) {
  const [profile, setProfile] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [updatedProfile, setUpdatedProfile] = useState({
    avatar: "",
    bio: "",
  });

  useEffect(() => {
    // Fetch the user's profile
    fetch(`/users/${userId}`)
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
        throw new Error("Failed to fetch profile");
      })
      .then((data) => {
        setProfile(data);
        setUpdatedProfile({ avatar: data.avatar, bio: data.bio });
      })
      .catch((error) => console.error(error));
  }, [userId]);

  const handleSave = () => {
    // Update profile on the server
    fetch(`/users/${userId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updatedProfile),
    })
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
        throw new Error("Failed to update profile");
      })
      .then((data) => {
        setProfile(data);
        setEditMode(false);
      })
      .catch((error) => {
        console.error(error);
        alert("An error occurred while updating the profile.");
      });
  };

  if (!profile) {
    return <p>Loading profile...</p>;
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Profile</h1>
      <div style={styles.profileCard}>
        <img
          src={profile.avatar}
          alt="Profile Avatar"
          style={styles.avatar}
        />
        {editMode ? (
          <>
            <input
              type="text"
              style={styles.input}
              value={updatedProfile.avatar}
              onChange={(e) =>
                setUpdatedProfile({ ...updatedProfile, avatar: e.target.value })
              }
              placeholder="Avatar URL"
            />
            <textarea
              style={styles.textarea}
              value={updatedProfile.bio}
              onChange={(e) =>
                setUpdatedProfile({ ...updatedProfile, bio: e.target.value })
              }
              placeholder="Bio"
            />
          </>
        ) : (
          <>
            <h2>{profile.username}</h2>
            <p style={styles.bio}>{profile.bio}</p>
          </>
        )}
        {editMode ? (
          <button style={styles.button} onClick={handleSave}>
            Save
          </button>
        ) : (
          <button style={styles.button} onClick={() => setEditMode(true)}>
            Edit Profile
          </button>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
    margin: "20px auto",
    padding: "20px",
    border: "1px solid #ccc",
    borderRadius: "10px",
    backgroundColor: "#f9f9f9",
  },
  header: {
    textAlign: "center",
    marginBottom: "20px",
  },
  profileCard: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  avatar: {
    width: "100px",
    height: "100px",
    borderRadius: "50%",
    marginBottom: "10px",
  },
  bio: {
    margin: "10px 0",
    fontStyle: "italic",
    textAlign: "center",
  },
  input: {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  textarea: {
    width: "100%",
    padding: "10px",
    margin: "10px 0",
    borderRadius: "5px",
    border: "1px solid #ccc",
  },
  button: {
    backgroundColor: "#007bff",
    color: "#fff",
    padding: "10px 20px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    marginTop: "10px",
  },
};

export default Profile;
