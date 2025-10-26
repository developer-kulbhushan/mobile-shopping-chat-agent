import { useState } from 'react';
import { LandingPage } from './components/LandingPage';
import { ChatInterface } from './components/ChatInterface';
import { apiService } from './services/api.service';

function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [isCreatingSession, setIsCreatingSession] = useState(false);

  const handleStartChat = async () => {
    setIsCreatingSession(true);
    try {
      const response = await apiService.createSession();
      setSessionId(response.session_id);
    } catch (error) {
      console.error('Error creating session:', error);
      alert('Failed to start chat. Please try again.');
    } finally {
      setIsCreatingSession(false);
    }
  };

  const handleNewChat = async () => {
    if (sessionId) {
      try {
        await apiService.deleteSession(sessionId);
      } catch (error) {
        console.error('Error deleting session:', error);
      }
    }
    await handleStartChat();
  };

  if (isCreatingSession) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent mb-4"></div>
          <p className="text-gray-600 font-medium">Starting chat session...</p>
        </div>
      </div>
    );
  }

  if (!sessionId) {
    return <LandingPage onStartChat={handleStartChat} />;
  }

  return <ChatInterface sessionId={sessionId} onNewChat={handleNewChat} />;
}

export default App;
