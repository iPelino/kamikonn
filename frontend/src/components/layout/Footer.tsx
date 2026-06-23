import { Link } from 'react-router';

export default function Footer() {
  return (
    <footer className="border-t bg-forest py-8 text-sage md:py-12">
      <div className="container flex flex-col items-center justify-between gap-4 px-4 md:flex-row md:px-6">
        <div className="flex flex-col items-center gap-2 md:items-start">
          <span className="font-heading text-xl font-bold">
            <span className="text-sage">Kami</span>
            <span className="text-amber">Konn</span>
          </span>
          <p className="text-center text-sm text-sage/80 md:text-left">
            Connecting Rwanda's academic ecosystem.
          </p>
        </div>

        <div className="flex gap-4 text-sm font-medium">
          <Link to="/about" className="hover:text-amber">About</Link>
          <Link to="/contact" className="hover:text-amber">Contact</Link>
          <Link to="/privacy" className="hover:text-amber">Privacy</Link>
        </div>

        <p className="text-sm text-sage/60">
          © {new Date().getFullYear()} KamiKonn. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
