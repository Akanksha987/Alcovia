import { Star } from "lucide-react";

export default function SocialProof() {
  return (
    <div className="p-6 bg-gray-50 text-center">
      <div className="flex justify-center mb-2">
        {[...Array(5)].map((_, i) => (
          <Star key={i} className="text-yellow-400" />
        ))}
      </div>
      <p>Rated 4.8/5 by 2,354 satisfied customers</p>
      <p className="mt-2 text-green-600 text-sm">✔ Verified Purchase | ✔ Trusted Brand</p>
    </div>
  );
}
