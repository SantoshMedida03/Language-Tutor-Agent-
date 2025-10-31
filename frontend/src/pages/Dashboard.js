import React, { useState, useEffect, useCallback } from 'react';
import Header from '../components/Header';
import Chat from '../components/Chat';
import Story from '../components/Story';
import Quiz from '../components/Quiz';
import Vocabulary from '../components/Vocabulary';
import Progress from '../components/Progress';
import api from '../services/api';

const Dashboard = () => {
  const [story, setStory] = useState(null);
  const [quiz, setQuiz] = useState(null);

  // This function runs only once on initial load to get or create the session
  useEffect(() => {
    const loadTodaySession = async () => {
      try {
        const response = await api.get('/session/today');
        setStory(response.data.story || null);
        setQuiz(response.data.quiz || null);
      } catch (error) {
        console.error("Failed to load today's session", error);
        setStory(null);
        setQuiz(null);
      }
    };
    loadTodaySession();
  }, []);

  // This function is for refreshing the quiz after a chat interaction
  const refreshData = useCallback(async () => {
    try {
      const quizResponse = await api.get('/quiz');
      setQuiz(quizResponse.data && quizResponse.data.id ? quizResponse.data : null);
    } catch (error) {
      console.error("Failed to refresh quiz data", error);
    }
  }, []);

  return (
    <div className="flex flex-col bg-gray-100">
      <Header />
      <main className="flex-grow container mx-auto p-4 lg:p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <div className="lg:col-span-2">
            <Chat onDataUpdate={refreshData} />
          </div>

          <div className="flex flex-col gap-6">
            <Story story={story} />
            <Quiz quiz={quiz} />
            <Vocabulary />
            <Progress />
          </div>

        </div>
      </main>
    </div>
  );
};

export default Dashboard;
