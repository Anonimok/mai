import React from "react";
import "./globals.css";
import { cn } from "@/lib/utils";

// Since this is a Vite/React project, not Next.js, we use a standard HTML structure.
// We can apply global styles and fonts via globals.css

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Gerador de Grade Horária</title> {/* You can customize the title */}
        {/* Link to fonts or other head elements can go here if needed */}
      </head>
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased",
          // If you were using a specific font like Inter, you would set it up in globals.css or here via a className
        )}
      >
        {children}
      </body>
    </html>
  );
}

