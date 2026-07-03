import { useParams, Link } from 'react-router';
import { Button } from '@/components/ui/button';
import { Building2 } from 'lucide-react';
import { SEO } from '@/components/SEO';

export default function UniversityProfilePage() {
  const { slug } = useParams<{ slug: string }>();

  const displayName = slug
    ? slug.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
    : 'University';

  return (
    <div className="container mx-auto px-4 py-8">
      <SEO title={displayName} />

      <div className="mb-8 flex items-center gap-4">
        <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-forest/10">
          <Building2 className="h-7 w-7 text-forest" />
        </div>
        <div>
          <h1 className="font-heading text-3xl font-bold tracking-tight text-forest">
            {displayName}
          </h1>
          <p className="mt-1 text-sm text-charcoal/60">University profile</p>
        </div>
      </div>

      <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-forest/20 bg-sage/50 py-20 text-center">
        <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-forest/10">
          <Building2 className="h-7 w-7 text-forest/50" />
        </div>
        <p className="mb-2 text-base font-medium text-charcoal">No events yet</p>
        <p className="mb-6 max-w-xs text-sm text-charcoal/60">
          Events from this university will appear here once they are published.
        </p>
        <Button asChild variant="outline" className="border-forest text-forest hover:bg-forest/5">
          <Link to="/events">Browse All Events</Link>
        </Button>
      </div>
    </div>
  );
}
