import { useState, useEffect } from "react";

export default function LiveCounter() {
  const [viewers, setViewers] = useState(27);

  useEffect(() => {
    const interval = setInterval(() => {
      setViewers((prev) => prev + Math.floor(Math.random() * 3 - 1));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-yellow-100 p-4 text-center text-sm">
      🔥 {viewers} people are viewing this product now
    </div>
  );
}
