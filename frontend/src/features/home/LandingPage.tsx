import { Link } from 'react-router';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { SEO } from '@/components/SEO';
import { useEvents } from '@/features/events/hooks/useEvents';
import { EventCard } from '@/features/events/components/EventCard';
import { EventGridSkeleton } from '@/components/skeletons/EventSkeletons';
import { ArrowRight, MapPin, Users, Calendar, Sparkles } from 'lucide-react';

// Rwanda's major Kigali universities
const UNIVERSITIES = [
  'ALU',
  'UR',
  'KIST',
  'ULK',
  'KIM',
  'SFB',
  'INES',
  'AUCA',
  'GIMPA',
  'IPRC',
];

const STATS = [
  { icon: Calendar, label: 'Events this semester', value: '120+' },
  { icon: Users, label: 'Active students', value: '5,000+' },
  { icon: MapPin, label: 'Universities', value: '10' },
];

export function LandingPage() {
  const { data: eventsData, isLoading } = useEvents({ status: 'APPROVED', ordering: '-start_time' });
  const featuredEvents = eventsData?.results?.slice(0, 6) ?? [];

  return (
    <>
      <SEO
        title="KamiKonn — Academic Events Across Rwanda"
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
      />

      {/* ── Hero ────────────────────────────────────────────── */}
      <section
        className="relative overflow-hidden rounded-2xl bg-forest text-sage mb-12 px-6 py-16 md:py-24 md:px-12"
        aria-labelledby="hero-heading"
      >
        {/* Subtle decorative ring */}
        <div
          className="pointer-events-none absolute -top-24 -right-24 h-96 w-96 rounded-full bg-amber/10 blur-3xl"
          aria-hidden="true"
        />
        <div
          className="pointer-events-none absolute -bottom-16 -left-16 h-64 w-64 rounded-full bg-sage/5 blur-2xl"
          aria-hidden="true"
        />

        <div className="relative max-w-2xl">
          <Badge className="mb-4 bg-amber/20 text-amber border-amber/30 hover:bg-amber/20">
            <Sparkles className="h-3 w-3 mr-1" aria-hidden="true" />
            Connecting Kigali&apos;s 10 universities
          </Badge>

          <h1
            id="hero-heading"
            className="font-heading text-4xl font-bold leading-tight tracking-tight md:text-5xl lg:text-6xl"
          >
            Discover Academic Events Across{' '}
            <span className="text-amber">Rwanda</span>
          </h1>

          <p className="mt-5 text-lg text-sage/80 leading-relaxed max-w-xl">
            The central hub for seminars, hackathons, workshops, and networking
            events happening at Kigali&apos;s universities — all in one place.
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/events">
              <Button
                size="lg"
                className="bg-amber text-forest hover:bg-amber/90 font-semibold cursor-pointer transition-colors duration-200"
              >
                Explore Events
                <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
              </Button>
            </Link>
            <Link to="/events/create">
              <Button
                size="lg"
                variant="outline"
                className="border-sage/40 text-sage hover:bg-sage/10 cursor-pointer transition-colors duration-200"
              >
                Submit an Event
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* ── Stats strip ─────────────────────────────────────── */}
      <section
        className="mb-12 grid grid-cols-3 gap-4 rounded-xl bg-white dark:bg-card border p-6"
        aria-label="Platform statistics"
      >
        {STATS.map(({ icon: Icon, label, value }) => (
          <div key={label} className="flex flex-col items-center text-center gap-1">
            <Icon className="h-6 w-6 text-primary mb-1" aria-hidden="true" />
            <span className="text-2xl font-bold font-heading text-primary">{value}</span>
            <span className="text-xs text-muted-foreground">{label}</span>
          </div>
        ))}
      </section>

      {/* ── Featured Events ──────────────────────────────────── */}
      <section aria-labelledby="featured-heading" className="mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 id="featured-heading" className="font-heading text-2xl font-bold tracking-tight">
            Upcoming Events
          </h2>
          <Link
            to="/events"
            className="text-sm text-primary hover:underline flex items-center gap-1 font-medium cursor-pointer"
          >
            View all
            <ArrowRight className="h-3.5 w-3.5" aria-hidden="true" />
          </Link>
        </div>

        {isLoading ? (
          <EventGridSkeleton count={6} />
        ) : featuredEvents.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredEvents.map((event) => (
              <EventCard key={event.id} event={event} />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-dashed bg-muted/30 py-16 text-center">
            <Calendar className="mx-auto h-10 w-10 text-muted-foreground mb-3" aria-hidden="true" />
            <p className="text-muted-foreground font-medium">No upcoming events yet.</p>
            <Link to="/events/create" className="mt-3 inline-block text-sm text-primary hover:underline cursor-pointer">
              Be the first to submit one
            </Link>
          </div>
        )}
      </section>

      {/* ── University Strip ─────────────────────────────────── */}
      <section
        className="rounded-xl bg-white dark:bg-card border p-8 text-center"
        aria-labelledby="universities-heading"
      >
        <h2 id="universities-heading" className="font-heading text-xl font-semibold mb-2">
          Representing all major Kigali universities
        </h2>
        <p className="text-sm text-muted-foreground mb-6">
          Events from 10 institutions, discoverable in one place.
        </p>
        <div className="flex flex-wrap gap-2 justify-center">
          {UNIVERSITIES.map((uni) => (
            <Badge
              key={uni}
              variant="outline"
              className="px-3 py-1 text-sm cursor-pointer hover:bg-primary hover:text-primary-foreground transition-colors duration-150"
            >
              {uni}
            </Badge>
          ))}
        </div>
        <div className="mt-6">
          <Link to="/universities">
            <Button variant="outline" className="cursor-pointer">
              Browse by University
            </Button>
          </Link>
        </div>
      </section>
    </>
  );
}
