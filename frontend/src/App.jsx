import { useState, useRef, useEffect } from "react";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! I am the Ogaranya Support Bot. How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_text: userMessage }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Something went wrong on the server.");
      }

      const data = await response.json();
      setMessages((prev) => [...prev, { sender: "bot", text: data.reply }]);

    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: `⚠️ Error: ${error.message}`, isError: true },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    // Deep dark background for the entire app
    <div className="flex flex-col h-screen bg-gray-950 text-gray-100 font-sans selection:bg-indigo-500/30">

      {/* Header - Glassmorphism effect */}
      <header className="sticky top-0 z-10 bg-gray-900/70 backdrop-blur-md border-b border-gray-800 p-5 flex items-center justify-center shadow-lg">
        <h1 className="text-xl font-bold flex items-center gap-3">
          <span className="text-2xl drop-shadow-md">🤖</span>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            Ogaranya Support
          </span>
        </h1>
      </header>

      {/* Chat History Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 flex flex-col gap-6 w-full max-w-4xl mx-auto custom-scrollbar">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            {/* Bot Avatar (Optional, adds a nice touch) */}
            {msg.sender === "bot" && (
              <div className="w-8 h-8 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center mr-3 mt-1 flex-shrink-0">
                <span className="text-sm">🤖</span>
              </div>
            )}

            <div
              className={`max-w-[85%] md:max-w-[75%] px-5 py-3.5 rounded-2xl shadow-sm text-[15px] ${
                msg.sender === "user"
                  ? "bg-gradient-to-tr from-indigo-600 to-blue-500 text-white rounded-br-sm shadow-indigo-900/20" // User bubble: vibrant gradient
                  : msg.isError
                  ? "bg-red-900/30 text-red-300 border border-red-800/50 rounded-bl-sm" // Error bubble
                  : "bg-gray-800 text-gray-200 border border-gray-700/50 rounded-bl-sm leading-relaxed" // Bot bubble: sleek dark gray
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex justify-start items-end">
             <div className="w-8 h-8 rounded-full bg-gray-800 border border-gray-700 flex items-center justify-center mr-3 flex-shrink-0">
                <span className="text-sm">🤖</span>
              </div>
            <div className="bg-gray-800 border border-gray-700/50 rounded-2xl rounded-bl-sm px-5 py-4 flex gap-1.5 items-center">
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
              <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </main>

      {/* Input Area - Glassmorphism effect */}
      <footer className="bg-gray-900/80 backdrop-blur-md border-t border-gray-800 p-4 pb-6 md:pb-4">
        <form
          onSubmit={handleSendMessage}
          className="max-w-4xl mx-auto flex gap-3 relative"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1 bg-gray-950/50 border border-gray-700 text-gray-100 placeholder-gray-500 focus:bg-gray-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-2xl px-5 py-4 outline-none transition-all disabled:opacity-50 shadow-inner"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-indigo-600 text-white px-7 py-4 rounded-2xl font-semibold hover:bg-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center shadow-lg shadow-indigo-900/20 active:scale-95"
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              "Send"
            )}
          </button>
        </form>
      </footer>

    </div>
  );
}

export default App;