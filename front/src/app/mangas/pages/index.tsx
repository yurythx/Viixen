import Header from '../components/Header';
import Hero from '../components/Hero';
import FeaturedManga from '../components/FeaturedManga';

export default function Home() {
  return (
    <>
      <Header />
      <Hero />
      <main className="container">
        <section>
          <FeaturedManga />
        </section>
      </main>
    </>
  );
}