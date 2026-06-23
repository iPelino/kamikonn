import { Link } from 'react-router';
import { Button } from '@/components/ui/button';
import MobileNav from './MobileNav';

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-forest text-sage shadow-sm">
      <div className="container flex h-16 items-center px-4 md:px-6">
        <div className="mr-4 flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <span className="font-heading text-xl font-bold">
              <span className="text-sage">Kami</span>
              <span className="text-amber">Konn</span>
            </span>
          </Link>
          <nav className="hidden items-center space-x-6 text-sm font-medium md:flex">
            <Link to="/events" className="transition-colors hover:text-amber">
              Events
            </Link>
            <Link to="/universities" className="transition-colors hover:text-amber">
              Universities
            </Link>
          </nav>
        </div>
        
        <div className="flex flex-1 items-center justify-end space-x-4">
          <div className="hidden md:flex md:space-x-4">
            <Button variant="ghost" asChild className="text-sage hover:text-forest hover:bg-sage">
              <Link to="/login">Log in</Link>
            </Button>
            <Button className="bg-amber text-forest hover:bg-amber/90" asChild>
              <Link to="/register">Sign up</Link>
            </Button>
          </div>
          <MobileNav />
        </div>
      </div>
    </header>
  );
}
