import { Link } from 'react-router';
import { Button } from '@/components/ui/button';
import { Bookmark } from 'lucide-react';
import { SEO } from '@/components/SEO';

export default function SavedEventsPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <SEO title="Saved Events" />
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold tracking-tight text-forest">
          Saved Events
        </h1>
        <p className="mt-2 text-charcoal/70">
          Events you bookmark will appear here.
        </p>
      </div>

      <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-forest/20 bg-sage/50 py-20 text-center">
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-forest/10">
          <Bookmark className="h-7 w-7 text-forest/60" />
        </div>
        <p className="mb-2 text-base font-medium text-charcoal">No saved events yet</p>
        <p className="mb-6 max-w-xs text-sm text-charcoal/60">
          Events you save will appear here. Browse the discovery feed to find events worth bookmarking.
        </p>
        <Button asChild className="bg-forest text-white hover:bg-forest/90">
          <Link to="/events">Browse Events</Link>
        </Button>
      </div>
    </div>
  );
}
