// app/articles/layout.tsx
export default function ArticlesLayout({ children }: { children: React.ReactNode }) {
    return (
      <div>
        <h2>Artigos</h2>
        <div>{children}</div>
      </div>
    );
  }