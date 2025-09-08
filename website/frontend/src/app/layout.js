// Src/app/layout.js
import "./globals.css";

export const metadata = {
  title: "PoliWatch Hub",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
