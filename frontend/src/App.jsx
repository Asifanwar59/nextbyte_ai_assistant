import React, { useState } from 'react';
import { sendChatMessage } from "./services/api";
import { Send, RefreshCw, Bot, User, Loader2 } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isSyncing, setIsSyncing] = useState(false);
  const [isLoading, setIsLoading] = useState(false); // Track LLM response state

  const handleSyncData = async () => {
    setIsSyncing(true);
    try {
      const response = await fetch('http://localhost:8000/sync-data', { method: 'POST' });
      if (response.ok) alert("Started indexing local PDFs!");
    } catch (error) {
      console.error("Sync failed", error);
    } finally {
      setIsSyncing(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    // 1. Add User Message to UI
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      // 2. Call Backend API
      const response = await sendChatMessage(input);

      // 3. Extract the answer (ensure this matches your FastAPI response keys)
      // If your backend returns { "answer": "..." }, use response.data.answer
      const botAnswer = response.data.answer || response.data.response || "No response received.";

      // 4. Update UI with LLM response
      setMessages(prev => [...prev, { role: 'assistant', content: botAnswer }]);
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages(prev => [...prev, { role: 'assistant', content: "Error: Could not reach the AI assistant." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 p-4">
      <header className="flex justify-between items-center p-4 bg-white shadow rounded-lg mb-4">
        <h1 className="text-xl font-bold text-blue-600">Nextbyte AI Assistant</h1>
        <button
          onClick={handleSyncData}
          disabled={isSyncing}
          className="flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition disabled:bg-gray-400"
        >
          <RefreshCw size={18} className={isSyncing ? "animate-spin" : ""} />
          {isSyncing ? "Syncing..." : "Sync Local Data"}
        </button>
      </header>

      {/* Chat History Area */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-3 rounded-lg flex gap-3 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white shadow text-gray-800'}`}>
              {msg.role === 'assistant' ? <Bot size={20} className="shrink-0" /> : <User size={20} className="shrink-0" />}
              <p className="whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white shadow text-gray-800 p-3 rounded-lg flex gap-3">
              <Loader2 size={20} className="animate-spin text-blue-500" />
              <p className="italic text-sm text-gray-500">AI is thinking...</p>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white rounded-lg shadow mt-4 flex gap-2">
        <input
          className="flex-1 outline-none p-2"
          placeholder="Ask a question about your docs..."
          value={input}
          disabled={isLoading}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button
          onClick={handleSend}
          disabled={isLoading}
          className="bg-blue-500 p-2 text-white rounded hover:bg-blue-600 disabled:bg-gray-300"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}

export default App;
