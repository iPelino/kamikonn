import { Link, useNavigate } from 'react-router';
import { buttonVariants } from '@/components/ui/button';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { ModeToggle } from '@/components/mode-toggle';
import MobileNav from './MobileNav';
import { useAuthStore } from '@/stores/authStore';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { LayoutDashboard, CalendarCheck, LogOut, User } from 'lucide-react';

function UserMenu() {
  const { user, clearAuth } = useAuthStore();
  const navigate = useNavigate();

  const initials = user
    ? `${user.first_name?.[0] ?? ''}${user.last_name?.[0] ?? ''}`.toUpperCase() || user.email[0].toUpperCase()
    : '';

  function handleLogout() {
    clearAuth();
    navigate('/');
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          className="relative h-9 w-9 rounded-full cursor-pointer hover:ring-2 hover:ring-amber transition-all"
          aria-label="Open user menu"
        >
          <Avatar className="h-9 w-9">
            <AvatarFallback className="bg-amber text-forest font-semibold text-sm">
              {initials}
            </AvatarFallback>
          </Avatar>
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuLabel className="font-normal">
          <div className="flex flex-col space-y-1">
            <p className="text-sm font-medium leading-none">
              {user?.first_name} {user?.last_name}
            </p>
            <p className="text-xs leading-none text-muted-foreground truncate">
              {user?.email}
            </p>
          </div>
        </DropdownMenuLabel>

        <DropdownMenuSeparator />

        <DropdownMenuItem asChild className="cursor-pointer">
          <Link to="/dashboard" className="flex items-center gap-2">
            <LayoutDashboard className="h-4 w-4" />
            My Dashboard
          </Link>
        </DropdownMenuItem>

        <DropdownMenuItem asChild className="cursor-pointer">
          <Link to="/my-rsvps" className="flex items-center gap-2">
            <CalendarCheck className="h-4 w-4" />
            My RSVPs
          </Link>
        </DropdownMenuItem>

        <DropdownMenuItem asChild className="cursor-pointer">
          <Link to="/notifications/preferences" className="flex items-center gap-2">
            <User className="h-4 w-4" />
            Notification Settings
          </Link>
        </DropdownMenuItem>

        <DropdownMenuSeparator />

        <DropdownMenuItem
          onClick={handleLogout}
          className="cursor-pointer text-destructive focus:text-destructive"
        >
          <LogOut className="h-4 w-4 mr-2" />
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default function Header() {
  const { isAuthenticated } = useAuthStore();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-forest text-sage shadow-sm">
      {/* Skip navigation link — only visible on keyboard focus */}
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>

      <div className="container flex h-16 items-center px-4 md:px-6">
        <div className="mr-4 flex">
          <Link to="/" className="mr-6 flex items-center space-x-2">
            <span className="font-heading text-xl font-bold">
              <span className="text-sage">Kami</span>
              <span className="text-amber">Konn</span>
            </span>
          </Link>

          <nav className="hidden items-center space-x-6 text-sm font-medium md:flex" aria-label="Main navigation">
            <Link to="/events" className="transition-colors hover:text-amber focus-visible:outline-none focus-visible:text-amber">
              Events
            </Link>
            <Link to="/universities" className="transition-colors hover:text-amber focus-visible:outline-none focus-visible:text-amber">
              Universities
            </Link>
          </nav>
        </div>

        <div className="flex flex-1 items-center justify-end space-x-3">
          {isAuthenticated ? (
            <UserMenu />
          ) : (
            <div className="hidden md:flex md:items-center md:space-x-3">
              <Link
                to="/login"
                className={cn(
                  buttonVariants({ variant: 'ghost' }),
                  'text-sage hover:text-forest hover:bg-sage cursor-pointer',
                )}
              >
                Log in
              </Link>
              <Link
                to="/register"
                className={cn(
                  buttonVariants({ variant: 'default' }),
                  'bg-amber text-forest hover:bg-amber/90 cursor-pointer',
                )}
              >
                Sign up
              </Link>
            </div>
          )}

          <ModeToggle />
          <MobileNav />
        </div>
      </div>
    </header>
  );
}
