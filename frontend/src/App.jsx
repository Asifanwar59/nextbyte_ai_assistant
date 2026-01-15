import React, { useState } from 'react';
import { uploadPDF, sendChatMessage } from './services/api';
import { Send, Upload, Bot, User } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (e) => {
    setIsUploading(true);
    try {
      await uploadPDF(e.target.files[0]);
      alert("PDF indexed successfully!");
    } catch (error) {
      console.error("Upload failed", error);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: 'user', content: input };
    setMessages([...messages, userMsg]);
    setInput("");

    try {
      const { data } = await sendChatMessage(input);
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error: Safety guardrail blocked this request." }]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50 p-4">
      <header className="flex justify-between items-center p-4 bg-white shadow rounded-lg mb-4">
        <h1 className="text-xl font-bold text-blue-600">Nextyte AI Assistant</h1>
        <label className="cursor-pointer flex items-center gap-2 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition">
          <Upload size={18} />
          {isUploading ? "Processing..." : "Upload PDF"}
          <input type="file" className="hidden" onChange={handleFileUpload} accept=".pdf" />
        </label>
      </header>

      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] p-3 rounded-lg flex gap-3 ${msg.role === 'user' ? 'bg-blue-600 text-white' : 'bg-white shadow text-gray-800'}`}>
              {msg.role === 'assistant' ? <Bot size={20} /> : <User size={20} />}
              <p>{msg.content}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 bg-white rounded-lg shadow mt-4 flex gap-2">
        <input
          className="flex-1 outline-none p-2"
          placeholder="Ask a question about your docs..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        />
        <button onClick={handleSend} className="bg-blue-500 p-2 text-white rounded hover:bg-blue-600">
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}

export default App;
