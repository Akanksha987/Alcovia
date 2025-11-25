export default function ProductGallery() {
  return (
    <div className="space-y-4">
      <img src="/product-main.jpg" className="rounded-lg shadow-lg w-full" />
      <div className="flex gap-2">
        <img src="/thumb1.jpg" className="w-20 h-20 rounded-md border" />
        <img src="/thumb2.jpg" className="w-20 h-20 rounded-md border" />
        <img src="/thumb3.jpg" className="w-20 h-20 rounded-md border" />
      </div>
    </div>
  );
}
