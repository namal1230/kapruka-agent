import { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import Header from "./components/Header";
import Globe from "./components/Globe";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "👋 Hi! I'm **Kapi**, your Kapruka shopping assistant!\n\nI can help you find gifts 🎁, check delivery 🚚, and complete your order 🛒\n\nWhat are you looking for today?",
    },
  ]);

  const [loading, setLoading] = useState<boolean>(false);

  const sendMessage = async (text: string): Promise<void> => {
    if (!text.trim() || loading) return;

    const userMessage: Message = { role: "user", content: text };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL || ""}/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages: updatedMessages }),
        }
      );

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "😅 Sorry, something went wrong. Please try again!",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative flex h-screen bg-gradient-to-br from-[#1a0533] via-[#2d1b69] to-[#1a0533] overflow-hidden">
      <Globe />
      <div className="relative z-10 flex flex-col w-full max-w-2xl mx-auto h-screen backdrop-blur-sm bg-black/30 border-x border-purple-900/30 shadow-2xl">
        <Header />
        <ChatWindow
          messages={messages}
          loading={loading}
          onSend={sendMessage}
        />
      </div>
    </div>
  );
}