import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Story = () => {
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStory = async () => {
      setError('');
      try {
        const response = await api.get('/story');
        setStory(response.data);
      } catch (err) {
        setError('Failed to load story.');
        console.error("Failed to fetch story", err);
      } finally {
        setLoading(false);
      }
    };

    fetchStory();
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md flex flex-col h-full">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Today's Story</h2>
      <div className="flex-grow overflow-y-auto">
        {loading ? (
          <p className="text-gray-500">Generating your story...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : story ? (
          <div>
            <h3 className="text-lg font-semibold text-blue-600">{story.title}</h3>
            <p className="text-gray-700 mt-2 whitespace-pre-line">{story.content}</p>
          </div>
        ) : (
          <p>No story available.</p>
        )}
      </div>
    </div>
  );
};

export default Story;