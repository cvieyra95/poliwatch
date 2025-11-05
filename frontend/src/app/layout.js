// Src/app/layout.js
import { SessionProvider } from "./components/SessionProvider";
import "./globals.css";

export const metadata = {
  title: "PoliWatch Hub",
};

export default function RootLayout({ children}) {
  return (
    
    <html lang="en">
      <body>
        <SessionProvider>
        {children}
        </SessionProvider>
        </body>
    </html>
  );
}
