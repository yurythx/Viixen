import Header from './mangas/components/Header';
import Hero from './mangas/components/Hero';
import FeaturedManga from './mangas/components/FeaturedManga';

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