
import Navbar from './core/components/Navbar'; // Caminho relativo
import Sidebar from './core/components/Sidebar';
import Footer from './core/components/Footer';
import { AnimatedContainer } from './core/components/AnimatedContainer';

const HomePage = () => {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1">
        <Navbar />
        <AnimatedContainer>
          <h1 className="text-center mt-10 text-4xl">Bem-vindo ao MangaVerse!</h1>
          <p className="text-center mt-4">Descubra e leia mangás em nossa plataforma.</p>
        </AnimatedContainer>
        <Footer />
      </div>
    </div>
  );
};

export default HomePage;