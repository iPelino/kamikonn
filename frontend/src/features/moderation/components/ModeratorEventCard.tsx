import { CalendarIcon, MapPinIcon, CheckIcon, XIcon } from 'lucide-react';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import type { Event } from '@/types/events';
import { useApproveEvent, useRejectEvent } from '../hooks/useModeration';
import { toast } from 'sonner';

interface ModeratorEventCardProps {
  event: Event;
}

export function ModeratorEventCard({ event }: ModeratorEventCardProps) {
  const approveMutation = useApproveEvent();
  const rejectMutation = useRejectEvent();

  const startDate = new Date(event.start_time).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  });

  const startTime = new Date(event.start_time).toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
  });

  const handleApprove = () => {
    approveMutation.mutate(event.slug, {
      onSuccess: () => {
        toast.success(`Event "${event.title}" approved successfully`);
      },
      onError: () => {
        toast.error('Failed to approve event');
      },
    });
  };

  const handleReject = () => {
    rejectMutation.mutate(event.slug, {
      onSuccess: () => {
        toast.success(`Event "${event.title}" rejected`);
      },
      onError: () => {
        toast.error('Failed to reject event');
      },
    });
  };

  return (
    <Card className="overflow-hidden flex flex-col h-full hover:shadow-lg transition-shadow border-forest/20">
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
          <Badge variant="destructive" className="animate-pulse">Pending Review</Badge>
          {event.category && <Badge variant="default">{event.category.name}</Badge>}
        </div>
      </div>

      <CardHeader className="p-4 pb-0 flex-grow">
        <h3 className="font-semibold text-lg line-clamp-2">{event.title}</h3>
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
        <div className="mt-2 text-xs">
          <strong>Universities:</strong>{' '}
          {event.universities?.map((u) => u.short_name).join(', ') || 'N/A'}
        </div>
      </CardContent>

      <CardFooter className="p-4 pt-0 flex gap-2 w-full">
        <Button
          variant="outline"
          className="w-1/2 border-red-200 text-red-600 hover:bg-red-50"
          onClick={handleReject}
          disabled={rejectMutation.isPending || approveMutation.isPending}
        >
          <XIcon className="w-4 h-4 mr-2" />
          Reject
        </Button>
        <Button
          className="w-1/2 bg-forest text-white hover:bg-forest/90"
          onClick={handleApprove}
          disabled={rejectMutation.isPending || approveMutation.isPending}
        >
          <CheckIcon className="w-4 h-4 mr-2" />
          Approve
        </Button>
      </CardFooter>
    </Card>
  );
}
