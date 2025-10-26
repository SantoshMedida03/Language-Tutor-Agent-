import React from 'react';
import Header from '../components/Header';
import Chat from '../components/Chat';
import Story from '../components/Story';
import Quiz from '../components/Quiz';
import Vocabulary from '../components/Vocabulary';
import Progress from '../components/Progress';

const Dashboard = () => {
  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Header />
      <main className="flex-grow container mx-auto p-4 lg:p-6 overflow-hidden">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
          
          {/* Main Content: Chat */}
          <div className="lg:col-span-2 h-[calc(100vh-120px)]">
            <Chat />
          </div>

          {/* Sidebar */}
          <div className="flex flex-col gap-6 h-[calc(100vh-120px)] overflow-y-auto">
            <Story />
            <Quiz />
            <Vocabulary />
            <Progress />
          </div>

        </div>
      </main>
    </div>
  );
};

export default Dashboard;