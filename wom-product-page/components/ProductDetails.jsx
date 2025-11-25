export default function ProductDetails() {
  return (
    <div className="space-y-4">
      <h1 className="text-3xl font-bold">Premium Lycra Stretchable Trousers</h1>
      <p className="text-gray-500">Polo Fit | Office Wear | Charcoal Black</p>
      <p className="text-2xl font-semibold">
        ₹1,299 <span className="text-red-500 line-through">₹2,599</span>
      </p>

      <button className="bg-black text-white px-6 py-3 rounded-lg hover:opacity-80">
        Add to Cart
      </button>
    </div>
  );
}
