import ProductCard from "./ProductCard";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function formatText(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br/>");
}

function parseProducts(content: string) {
  const jsonMatch = content.match(/```json([\s\S]*?)```/);
  if (jsonMatch) {
    try {
      const products = JSON.parse(jsonMatch[1].trim());
      if (Array.isArray(products)) return products;
    } catch {}
  }
  return null;
}

export default function MessageBubble({ message }: { message: Message }) {
  const isBot = message.role === "assistant";
  const products = isBot ? parseProducts(message.content) : null;
  const cleanContent = message.content
    .replace(/```json[\s\S]*?```/g, "")
    .trim();

  return (
    <div className={`flex ${isBot ? "justify-start" : "justify-end"}`}>
      {isBot && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-600 to-purple-400 flex items-center justify-center text-sm mr-2 flex-shrink-0 mt-1">
          🛍️
        </div>
      )}
      <div className={`max-w-[78%] ${!isBot && "items-end flex flex-col"}`}>
        <div
          className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
            isBot
              ? "bg-[#1e1535] text-purple-100 border border-purple-800/20 rounded-tl-sm"
              : "bg-gradient-to-br from-purple-600 to-purple-400 text-white rounded-tr-sm"
          }`}
          dangerouslySetInnerHTML={{ __html: formatText(cleanContent) }}
        />
        {products && products.length > 0 && (
          <div className="mt-3 grid grid-cols-2 gap-2 w-full">
            {products.map((p, i) => (
              <ProductCard key={i} product={p} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}