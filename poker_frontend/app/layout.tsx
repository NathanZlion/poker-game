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
        className={`${geistSans.variable} ${geistMono.variable} antialiased h-screen flex flex-col  border border-red-900 overflow-hidden`}
      >
        <Provider store={storeRef.current}>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {children}
          </ThemeProvider>
        </Provider>
      </body>
    </html>
  );
}
