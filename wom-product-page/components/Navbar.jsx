export default function Navbar() {
  return (
    <nav className="bg-black text-white py-4 px-6 flex justify-between">
      <h1 className="font-bold text-xl">Word of Mouth</h1>
      <div className="space-x-4">
        <a href="#" className="hover:underline">Home</a>
        <a href="#" className="hover:underline">Products</a>
        <a href="#" className="hover:underline">Contact</a>
      </div>
    </nav>
  );
}
