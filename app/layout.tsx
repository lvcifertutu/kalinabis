import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Kalinabis — Altar de Magia del Caos',
  description: 'Sistema ritual digital de magia del caos',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="es" className="scroll-smooth">
      <head>
        <meta charSet="UTF-8" />
        <meta name="theme-color" content="#0a0908" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Cinzel+Decorative:wght@400;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400;1,600&family=IM+Fell+English:ital@0;1&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="overflow-hidden">
        {children}
      </body>
    </html>
  );
}
