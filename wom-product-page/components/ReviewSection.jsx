export default function ReviewSection() {
  return (
    <div className="max-w-4xl mx-auto my-10 p-6">
      <h2 className="text-2xl font-bold mb-4">Customer Reviews</h2>
      <div className="space-y-3">
        <div className="p-4 border rounded-lg shadow-sm">
          ⭐⭐⭐⭐⭐
          <p>"Premium quality and very comfortable for office wear!"</p>
          <p className="text-sm text-gray-500">- Rahul Singh</p>
        </div>

        <div className="p-4 border rounded-lg shadow-sm">
          ⭐⭐⭐⭐☆
          <p>"Perfect fit and fabric. Value for money!"</p>
          <p className="text-sm text-gray-500">- Akanksha A.</p>
        </div>
      </div>
    </div>
  );
}
