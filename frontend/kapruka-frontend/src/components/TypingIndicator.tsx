export default function TypingIndicator() {
  return (
    <div className="flex justify-start items-end gap-2">
      <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center text-sm">
        🛍️
      </div>
      <div className="bg-[#1e1535] border border-purple-800/20 px-4 py-3 rounded-2xl rounded-tl-sm flex gap-1 items-center">
        <div className="dot w-2 h-2 bg-purple-400 rounded-full"></div>
        <div className="dot w-2 h-2 bg-purple-400 rounded-full"></div>
        <div className="dot w-2 h-2 bg-purple-400 rounded-full"></div>
      </div>
    </div>
  );
}