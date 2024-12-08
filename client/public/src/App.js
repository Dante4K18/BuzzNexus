import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Feed from './components/Feed';
import PostForm from './components/PostForm';

function App() {
    const [refreshFeed, setRefreshFeed] = useState(false);

    const handlePostCreated = () => {
        setRefreshFeed(!refreshFeed); // Trigger feed refresh
    };

    const userId = 1; // Replace with actual user ID from login or session

    return (
        <div>
             <Profile userId={userId} />
            <Navbar />
            <PostForm onPostCreated={handlePostCreated} />
            <Feed key={refreshFeed} />
        </div>
    );
}

export default App;
