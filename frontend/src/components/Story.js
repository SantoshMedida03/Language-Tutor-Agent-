import React from 'react';

const Story = ({ story }) => {
  return (
    <div className="p-6 bg-white rounded-lg shadow-md flex flex-col h-full">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Today's Story</h2>
      <div className="flex-grow overflow-y-auto">
        {!story ? (
          <p className="text-gray-500">No story available. Ask the tutor to generate one for you!</p>
        ) : (
          <div>
            <h3 className="text-lg font-semibold text-blue-600">{story.title}</h3>
            <p className="text-gray-700 mt-2 whitespace-pre-line">{story.content}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Story;