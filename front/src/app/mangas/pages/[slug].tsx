import { GetStaticPaths, GetStaticProps } from 'next';
import { useRouter } from 'next/router';
import styles from '../../core/styles/FeaturedManga.module.css';
import Image from 'next/image';

const mangas = [
  {
    title: 'One Piece',
    description: 'Monkey D. Luffy parte para se tornar o Rei dos Piratas.',
    status: 'Em andamento',
    rating: 9.8,
    image: '/mangas/one-piece.jpg',
  },
  {
    title: 'Naruto',
    description: 'Um ninja determinado busca reconhecimento e poder.',
    status: 'Completo',
    rating: 9.5,
    image: '/mangas/naruto.jpg',
  },
];

function slugify(str: string) {
  return str.toLowerCase().replace(/\s+/g, '-');
}

interface MangaProps {
  manga: {
    title: string;
    description: string;
    status: string;
    rating: number;
    image: string;
  };
}

export default function MangaPage({ manga }: MangaProps) {
  const router = useRouter();

  // Exibe o carregamento enquanto a página é gerada
  if (router.isFallback) {
    return <div>Carregando...</div>;
  }

  return (
    <div className={styles.mangaDetail}>
      <h1>{manga.title}</h1>
      <Image
        src={manga.image}
        alt={`Capa do mangá ${manga.title}`}
        width={300}
        height={250}
        className={styles.image}
      />
      <p>{manga.description}</p>
      <p>Status: <strong>{manga.status}</strong></p>
      <p>Avaliação: <strong>★ {manga.rating}</strong></p>
    </div>
  );
}

// Gera as páginas dinamicamente com base nos slugs
export const getStaticPaths: GetStaticPaths = async () => {
  const paths = mangas.map((manga) => ({
    params: { slug: slugify(manga.title) },
  }));

  return { paths, fallback: true };
};

// Recupera os dados do mangá com base no slug
export const getStaticProps: GetStaticProps = async ({ params }) => {
  const slug = params?.slug as string;
  const manga = mangas.find((m) => slugify(m.title) === slug);

  if (!manga) {
    return { notFound: true };
  }

  return {
    props: {
      manga,
    },
  };
};