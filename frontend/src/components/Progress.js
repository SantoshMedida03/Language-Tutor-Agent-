import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Progress = () => {
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProgress = async () => {
      setError('');
      try {
        const response = await api.get('/progress');
        setProgress(response.data);
      } catch (err) {
        setError('Failed to load progress.');
        console.error("Failed to fetch progress", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProgress();
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-800">My Progress</h2>
      <div className="max-h-48 overflow-y-auto">
        {loading ? (
          <p className="text-gray-500">Loading...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : progress.length > 0 ? (
          <ul className="space-y-2">
            {progress.map((item, index) => (
              <li key={index} className="text-sm text-gray-600 border-b pb-1">
                <span className="font-semibold">{item.date}:</span> {item.words_learned} words learned (Quiz Accuracy: {item.quiz_accuracy * 100}%)
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No progress yet. Complete a quiz to see your progress!</p>
        )}
      </div>
    </div>
  );
};

export default Progress;