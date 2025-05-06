// app/layout.tsx
export const metadata = {
    title: 'MangaVerse',
    description: 'Portal definitivo para mangás, animes e cultura japonesa',
  };
  
  export default function RootLayout({
    children,
  }: {
    children: React.ReactNode;
  }) {
    return (
      <html lang="pt-BR">
        <body>{children}</body>
      </html>
    );
  }