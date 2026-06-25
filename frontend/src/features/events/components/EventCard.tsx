import { CalendarIcon, MapPinIcon } from 'lucide-react';
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
    <Card className="overflow-hidden flex flex-col h-full hover:shadow-lg transition-shadow">
      <div className="aspect-[2/1] relative bg-muted">
        {event.banner_image ? (
          <img
            src={event.banner_image}
            alt={event.title}
            className="object-cover w-full h-full"
          />
        ) : (
          <div className="flex items-center justify-center w-full h-full bg-secondary text-secondary-foreground">
            No Image Available
          </div>
        )}
        <div className="absolute top-2 right-2 flex gap-1">
          {event.is_virtual && <Badge variant="secondary">Virtual</Badge>}
          {event.category && <Badge variant="default">{event.category.name}</Badge>}
        </div>
      </div>

      <CardHeader className="p-4 pb-0 flex-grow">
        <Link to={`/events/${event.slug}`} className="hover:underline">
          <h3 className="font-semibold text-lg line-clamp-2">{event.title}</h3>
        </Link>
        <p className="text-sm text-muted-foreground line-clamp-2 mt-1">
          {event.description}
        </p>
      </CardHeader>

      <CardContent className="p-4 pt-4 space-y-2 text-sm text-muted-foreground">
        <div className="flex items-center gap-2">
          <CalendarIcon className="w-4 h-4" />
          <span>
            {startDate} at {startTime}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <MapPinIcon className="w-4 h-4" />
          <span className="line-clamp-1">{event.location}</span>
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0 flex items-center justify-between">
        <span className="font-medium text-primary">
          {parseFloat(event.price) === 0 ? 'Free' : `${event.price} RWF`}
        </span>
        <div className="text-xs text-muted-foreground">
          By {event.organizer.first_name} {event.organizer.last_name}
        </div>
      </CardFooter>
    </Card>
  );
}
