export default function Header() {
  return (
    <div className="flex items-center gap-3 px-5 py-4 bg-gradient-to-r from-[#2d1b69] to-[#4c1d95] border-b border-purple-800/30 shadow-lg">
      <div className="w-11 h-11 rounded-full bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center text-xl shadow-md">
        🛍️
      </div>
      <div>
        <h1 className="text-white font-bold text-lg leading-none">Kapru</h1>
        <span className="text-purple-300 text-xs">● Online — Kapruka Assistant</span>
      </div>
    </div>
  );
}