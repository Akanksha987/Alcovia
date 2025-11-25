import Navbar from "@/components/Navbar";
import ProductGallery from "@/components/ProductGallery";
import ProductDetails from "@/components/ProductDetails";
import LiveCounter from "@/components/LiveCounter";
import SocialProof from "@/components/SocialProof";
import ReviewSection from "@/components/ReviewSection";
import Comments from "@/components/Comments";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <div>
      <Navbar />
      <main className="max-w-7xl mx-auto p-6 grid md:grid-cols-2 gap-8">
        <ProductGallery />
        <ProductDetails />
      </main>

      <LiveCounter />
      <SocialProof />
      <ReviewSection />
      <Comments />
      <Footer />
    </div>
  );
}
