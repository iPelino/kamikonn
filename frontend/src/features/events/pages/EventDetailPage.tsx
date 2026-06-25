import { useParams, Link } from 'react-router';
import { useEventDetails } from '../hooks/useEvents';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { CalendarIcon, MapPinIcon, ArrowLeftIcon, GlobeIcon, Share2Icon } from 'lucide-react';
import { Loader2 } from 'lucide-react';

export function EventDetailPage() {
  const { slug } = useParams<{ slug: string }>();
  const { data: event, isLoading, isError } = useEventDetails(slug || '');

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <Loader2 className="h-10 w-10 animate-spin text-primary" />
      </div>
    );
  }

  if (isError || !event) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold mb-4">Event not found</h2>
        <p className="text-muted-foreground mb-8">The event you are looking for does not exist or has been removed.</p>
        <Link to="/events">
          <Button>Back to Events</Button>
        </Link>
      </div>
    );
  }

  const startDate = new Date(event.start_time).toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });

  const startTime = new Date(event.start_time).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
  });

  return (
    <article className="container mx-auto px-4 py-8 max-w-4xl">
      <Link to="/events" className="mb-6 -ml-4 inline-block">
        <Button variant="ghost">
          <ArrowLeftIcon className="mr-2 h-4 w-4" />
          Back to Events
        </Button>
      </Link>

      {/* Hero Image */}
      <div className="w-full aspect-video md:aspect-[21/9] bg-muted rounded-xl overflow-hidden mb-8 relative">
        {event.banner_image ? (
          <img
            src={event.banner_image}
            alt={event.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center w-full h-full text-muted-foreground text-xl">
            KamiKonn Event
          </div>
        )}
        <div className="absolute top-4 right-4 flex gap-2">
          {event.is_virtual && <Badge variant="secondary" className="text-sm shadow-md">Virtual Event</Badge>}
          {event.category && <Badge className="text-sm shadow-md">{event.category.name}</Badge>}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="md:col-span-2 space-y-8">
          <div>
            <h1 className="text-4xl font-bold tracking-tight mb-4">{event.title}</h1>
            <div className="prose prose-slate dark:prose-invert max-w-none">
              <p className="whitespace-pre-line text-muted-foreground leading-relaxed">
                {event.description}
              </p>
            </div>
          </div>

          <div className="space-y-4 pt-6 border-t">
            <h3 className="text-xl font-semibold">Participating Universities</h3>
            <div className="flex flex-wrap gap-2">
              {event.universities?.map(u => (
                <Badge key={u.id} variant="outline" className="px-3 py-1">
                  {u.name}
                </Badge>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar Info */}
        <aside className="space-y-6">
          <div className="bg-card border rounded-xl p-6 space-y-6 shadow-sm">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <CalendarIcon className="w-5 h-5 text-primary mt-0.5" />
                <div>
                  <p className="font-medium">{startDate}</p>
                  <p className="text-muted-foreground text-sm">{startTime}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <MapPinIcon className="w-5 h-5 text-primary mt-0.5" />
                <div>
                  <p className="font-medium">{event.is_virtual ? 'Virtual' : 'Location'}</p>
                  <p className="text-muted-foreground text-sm">{event.location}</p>
                </div>
              </div>

              {event.is_virtual && event.virtual_link && (
                <div className="flex items-start gap-3">
                  <GlobeIcon className="w-5 h-5 text-primary mt-0.5" />
                  <div>
                    <p className="font-medium">Link</p>
                    <a href={event.virtual_link} target="_blank" rel="noreferrer" className="text-primary text-sm hover:underline">
                      Join Online
                    </a>
                  </div>
                </div>
              )}
            </div>

            <div className="pt-6 border-t space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Price</span>
                <span className="font-bold text-xl">
                  {parseFloat(event.price) === 0 ? 'Free' : `${event.price} RWF`}
                </span>
              </div>
              <Button className="w-full" size="lg">
                RSVP Now
              </Button>
              <Button variant="outline" className="w-full">
                <Share2Icon className="mr-2 h-4 w-4" /> Share Event
              </Button>
            </div>
          </div>

          <div className="text-sm text-center text-muted-foreground">
            Organized by <span className="font-medium text-foreground">{event.organizer.first_name} {event.organizer.last_name}</span>
          </div>
        </aside>
      </div>
    </article>
  );
}
