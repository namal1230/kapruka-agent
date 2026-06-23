import { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";
import TypingIndicator from "./TypingIndicator";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Props {
  messages: Message[];
  loading: boolean;
  onSend: (text: string) => void;
}

const SUGGESTIONS = [
  { label: "🎁 Popular gifts", text: "Show me popular gifts" },
  { label: "📦 Categories", text: "What categories do you have?" },
  { label: "🎂 Birthday cake", text: "I need a birthday cake" },
  { label: "🚚 Check delivery", text: "Can you deliver to Kandy?" },
  { label: "💐 Flowers", text: "Show me flowers" },
  { label: "📱 Electronics", text: "Show me electronics" },
];

export default function ChatWindow({ messages, loading, onSend }: Props) {
  const [input, setInput] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(true);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = () => {
    if (!input.trim()) return;
    setShowSuggestions(false);
    onSend(input);
    setInput("");
  };

  const handleSuggestion = (text: string) => {
    setShowSuggestions(false);
    onSend(text);
  };

  return (
    <>
      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>

      {showSuggestions && messages.length <= 1 && (
        <div className="px-4 pb-2 flex gap-2 overflow-x-auto">
          {SUGGESTIONS.map((s) => (
            <button
              key={s.label}
              onClick={() => handleSuggestion(s.text)}
              className="flex-shrink-0 bg-[#1e1535] border border-purple-700/40 text-purple-300 text-xs px-3 py-2 rounded-full hover:bg-[#2d1b69] transition-all"
            >
              {s.label}
            </button>
          ))}
        </div>
      )}

      <div className="px-4 py-3 border-t border-purple-900/40 bg-black/20 flex gap-3 items-center">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask me anything about Kapruka..."
          className="flex-1 bg-[#1e1535] border border-purple-800/40 rounded-full px-5 py-3 text-white text-sm placeholder-gray-500 outline-none focus:border-purple-500 transition-colors"
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="w-11 h-11 bg-gradient-to-br from-purple-600 to-purple-400 rounded-full flex items-center justify-center hover:scale-105 transition-transform disabled:opacity-50"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="white">
            <path d="M2 21l21-9L2 3v7l15 2-15 2v7z" />
          </svg>
        </button>
      </div>
    </>
  );
}