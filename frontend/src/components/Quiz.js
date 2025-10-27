import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Quiz = () => {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchQuiz = async () => {
      setError('');
      try {
        const response = await api.get('/quiz');
        setQuiz(response.data);
      } catch (err) {
        setError('Failed to load quiz.');
        console.error("Failed to fetch quiz", err);
      } finally {
        setLoading(false);
      }
    };

    fetchQuiz();
  }, []);

  const renderQuestions = () => {
    try {
      const questions = JSON.parse(quiz.questions);
      return questions.map((q, index) => (
        <div key={index} className="mt-3">
          <p className="font-medium">{index + 1}. {q.question}</p>
          {/* Placeholder for options/input */}
        </div>
      ));
    } catch (e) {
      return <p className="text-gray-700 mt-2">{quiz.questions}</p>;
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Comprehension Quiz</h2>
      {loading ? (
        <p className="text-gray-500">Loading quiz...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : quiz ? (
        <div>
          <h3 className="text-lg font-semibold text-blue-600">{quiz.title}</h3>
          {renderQuestions()}
          <button className="mt-4 w-full p-2 bg-green-500 text-white rounded-md hover:bg-green-600">
            Submit Answers
          </button>
        </div>
      ) : (
        <p>No quiz available.</p>
      )}
    </div>
  );
};

export default Quiz;