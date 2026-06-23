interface Product {
  name: string;
  price: number;
  image?: string;
  url?: string;
  currency?: string;
}

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  return (
    <div
      className="bg-[#2d1b69] border border-purple-700/30 rounded-xl overflow-hidden cursor-pointer hover:-translate-y-1 transition-transform"
      onClick={() => product.url && window.open(product.url, "_blank")}
    >
      {product.image && (
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-28 object-cover"
          onError={(e) =>
            ((e.target as HTMLImageElement).style.display = "none")
          }
        />
      )}
      <div className="p-2">
        <p className="text-purple-100 text-xs font-semibold line-clamp-2 mb-1">
          {product.name}
        </p>
        <p className="text-purple-400 text-sm font-bold">
          {product.currency || "LKR"} {product.price?.toLocaleString()}
        </p>
        <button className="mt-2 w-full bg-purple-600 hover:bg-purple-500 text-white text-xs py-1.5 rounded-lg transition-colors">
          View Product →
        </button>
      </div>
    </div>
  );
}