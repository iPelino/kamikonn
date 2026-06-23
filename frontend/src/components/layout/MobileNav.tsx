import { Menu } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function MobileNav() {
  return (
    <div className="md:hidden">
      <Button variant="ghost" size="icon" className="text-sage hover:bg-forest-light">
        <Menu className="h-6 w-6" />
        <span className="sr-only">Toggle menu</span>
      </Button>
    </div>
  );
}
