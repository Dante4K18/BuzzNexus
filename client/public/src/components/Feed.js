// client/src/components/Feed.js
import React, { useState, useEffect } from 'react';

function Feed() {
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        fetch('/posts')
            .then(res => res.json())
            .then(data => setPosts(data));
    }, []);

    return (
        <div>
            {posts.map((post, index) => (
                <div key={index}>
                    <h3>{post.user}</h3>
                    <p>{post.content}</p>
                </div>
            ))}
        </div>
    );
}

export default Feed;
