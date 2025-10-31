import React, { useState, useEffect } from 'react';
import api from '../services/api';

const Quiz = ({ quiz }) => {
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [score, setScore] = useState(null);
  const [suggestion, setSuggestion] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Reset state when a new quiz is passed in
  useEffect(() => {
    setSelectedAnswers({});
    setScore(null);
    setSuggestion('');
  }, [quiz]);

  const handleAnswerChange = (questionIndex, answer) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [questionIndex]: answer,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const response = await api.post('/quiz/submit', selectedAnswers);
      setScore(response.data.score);
      setSuggestion(response.data.suggestion);
    } catch (error) {
      console.error("Failed to submit quiz", error);
      // Handle error display to the user
    } finally {
      setSubmitting(false);
    }
  };

  const renderQuestions = () => {
    if (!quiz || !quiz.questions) return null;
    try {
      const questions = JSON.parse(quiz.questions);
      return questions.map((q, index) => {
        const questionParts = q.split('\n');
        const questionText = questionParts[0];
        const choices = questionParts.slice(1);
        return (
          <div key={index} className="mt-4">
            <p className="font-medium">{index + 1}. {questionText}</p>
            <div className="flex flex-col mt-2 space-y-2">
              {choices.map((choice, choiceIndex) => (
                <label key={choiceIndex} className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name={`question-${index}`}
                    value={choice}
                    onChange={() => handleAnswerChange(index, choice)}
                    checked={selectedAnswers[index] === choice}
                    className="mr-2"
                    disabled={score !== null}
                  />
                  <span>{choice}</span>
                </label>
              ))}
            </div>
          </div>
        );
      });
    } catch (e) {
      console.error("Failed to parse quiz questions", e);
      return <p className="text-red-500">Error displaying quiz questions.</p>;
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Comprehension Quiz</h2>
      {!quiz ? (
        <p className="text-gray-500">No quiz available. Ask the tutor to generate one after a story!</p>
      ) : score !== null ? (
        <div className="text-center">
          <h3 className="text-lg font-semibold text-blue-600">Quiz Complete!</h3>
          <p className="text-2xl font-bold mt-4">Your Score: {score.toFixed(2)}%</p>
          <p className="text-gray-700 mt-4">{suggestion}</p>
        </div>
      ) : (
        <div>
          <h3 className="text-lg font-semibold text-blue-600">{quiz.title}</h3>
          <form onSubmit={handleSubmit}>
            {renderQuestions()}
            <button type="submit" className="mt-6 w-full p-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:bg-gray-400" disabled={submitting}>
              {submitting ? 'Submitting...' : 'Submit Answers'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Quiz;