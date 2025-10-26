import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Vocabulary = () => {
  const [vocab, setVocab] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchVocab = async () => {
      setError('');
      try {
        const response = await api.get('/vocab');
        setVocab(response.data);
      } catch (err) {
        setError('Failed to load vocabulary.');
        console.error("Failed to fetch vocabulary", err);
      } finally {
        setLoading(false);
      }
    };

    fetchVocab();
  }, []);

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-800">My Vocabulary</h2>
      <div className="max-h-48 overflow-y-auto">
        {loading ? (
          <p className="text-gray-500">Loading...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : vocab.length > 0 ? (
          <ul className="space-y-2">
            {vocab.map((item, index) => (
              <li key={index} className="border-b pb-1">
                <p className="font-semibold text-gray-700">{item.word}</p>
                <p className="text-sm text-gray-600">{item.meaning}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No vocabulary yet. Start chatting to build your list!</p>
        )}
      </div>
    </div>
  );
};

export default Vocabulary;