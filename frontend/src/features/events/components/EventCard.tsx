import { CalendarIcon, MapPinIcon, Calendar } from 'lucide-react';
import { Link } from 'react-router';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { Event } from '@/types/events';

interface EventCardProps {
  event: Event;
}

export function EventCard({ event }: EventCardProps) {
  const startDate = new Date(event.start_time).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  const startTime = new Date(event.start_time).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
  });

  return (
    // Entire card is the link — clicking anywhere navigates to the event
    <Link
      to={`/events/${event.slug}`}
      className="block h-full cursor-pointer group focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-lg"
    >
      <Card className="overflow-hidden flex flex-col h-full transition-shadow duration-200 group-hover:shadow-lg">
        {/* Banner image */}
        <div className="aspect-[2/1] relative bg-muted overflow-hidden">
          {event.banner_image ? (
            <img
              src={event.banner_image}
              alt={event.title}
              className="object-cover w-full h-full transition-transform duration-300 group-hover:scale-[1.02]"
              loading="lazy"
              decoding="async"
            />
          ) : (
            // Branded gradient fallback — not raw text
            <div className="flex flex-col items-center justify-center w-full h-full bg-gradient-to-br from-forest/10 to-amber/10 text-forest/40 gap-2">
              <Calendar className="h-8 w-8" aria-hidden="true" />
              <span className="text-xs font-medium">KamiKonn Event</span>
            </div>
          )}

          {/* Badges overlay */}
          <div className="absolute top-2 right-2 flex gap-1">
            {event.is_virtual && <Badge variant="secondary">Virtual</Badge>}
            {event.category && <Badge variant="default">{event.category.name}</Badge>}
          </div>
        </div>

        {/* Title + description */}
        <CardHeader className="p-4 pb-0 flex-grow">
          <h3 className="font-semibold text-lg line-clamp-2 group-hover:text-primary transition-colors duration-150">
            {event.title}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
            {event.description}
          </p>
        </CardHeader>

        {/* Date + location meta */}
        <CardContent className="p-4 pt-4 space-y-2 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <CalendarIcon className="w-4 h-4 shrink-0" aria-hidden="true" />
            <span>
              {startDate} at {startTime}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <MapPinIcon className="w-4 h-4 shrink-0" aria-hidden="true" />
            <span className="line-clamp-1">{event.location}</span>
          </div>
        </CardContent>

        {/* Price + organizer footer */}
        <CardFooter className="p-4 pt-0 flex items-center justify-between">
          <span className="font-semibold text-primary">
            {parseFloat(event.price) === 0 ? 'Free' : `${event.price} RWF`}
          </span>
          {/* Organizer links to their profile page */}
          <span
            className="text-xs text-muted-foreground hover:text-foreground transition-colors duration-150"
            onClick={(e) => {
              // Prevent the card-level Link from firing when clicking organizer
              e.preventDefault();
              e.stopPropagation();
              window.location.href = `/organizer/${event.organizer.id}`;
            }}
            role="link"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                window.location.href = `/organizer/${event.organizer.id}`;
              }
            }}
          >
            By {event.organizer.first_name} {event.organizer.last_name}
          </span>
        </CardFooter>
      </Card>
    </Link>
  );
}
