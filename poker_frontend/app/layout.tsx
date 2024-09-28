'use client'

import localFont from "next/font/local";
import "./globals.css";
import { ThemeProvider } from "@/providers/ThemeProvider";
import { ThemeToggle } from "@/components/common/ThemeToggle";
import { makeStore, AppStore } from '../lib/store'
import { useRef } from "react";
import { Provider } from "react-redux";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});


export default function RootLayout({

  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const storeRef = useRef<AppStore>();
  if (!storeRef.current) {
    // Create the store instance the first time this renders
    storeRef.current = makeStore()
  }

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen flex flex-col `}
      >
        <Provider store={storeRef.current}>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <nav className="flex justify-end p-5 pe-10"> <ThemeToggle /> </nav>

            {children}
          </ThemeProvider>
        </Provider>
      </body>
    </html>
  );
}
