import { useQuery } from '@tanstack/react-query';
import { listMyRSVPs } from '../api/rsvpApi';
import type { RSVP } from '../api/rsvpApi';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Loader2, CalendarIcon, MapPinIcon, Download } from 'lucide-react';
import { downloadCalendar } from '../api/rsvpApi';
import { toast } from 'sonner';
import { Link } from 'react-router';

function statusBadge(status: RSVP['status']) {
  if (status === 'ATTENDING') {
    return (
      <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
        Attending
      </Badge>
    );
  }
  if (status === 'WAITLISTED') {
    return (
      <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200">
        Waitlisted
      </Badge>
    );
  }
  return <Badge variant="secondary">Cancelled</Badge>;
}

export function MyRSVPsPage() {
  const { data: rsvps = [], isLoading } = useQuery({
    queryKey: ['my-rsvps'],
    queryFn: listMyRSVPs,
  });

  const handleDownload = async (rsvpId: string) => {
    try {
      await downloadCalendar(rsvpId);
      toast.success('Calendar file downloaded.');
    } catch {
      toast.error('Failed to download calendar.');
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">My RSVPs</h1>
        <p className="text-muted-foreground mt-1">Events you have registered for.</p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-16">
          <Loader2 className="h-8 w-8 animate-spin" />
        </div>
      ) : rsvps.length === 0 ? (
        <div className="text-center py-16 space-y-4">
          <p className="text-muted-foreground text-lg">You have not RSVPd to any events yet.</p>
          <Link to="/events">
            <Button>Browse Events</Button>
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {rsvps.map((rsvp) => (
            <Card key={rsvp.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-5">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 space-y-2">
                    <div className="flex items-center gap-3">
                      <Link
                        to={`/events/${rsvp.event_slug}`}
                        className="text-lg font-semibold hover:underline"
                      >
                        {rsvp.event_title ?? 'Event'}
                      </Link>
                      {statusBadge(rsvp.status)}
                    </div>

                    {rsvp.event_start_time && (
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <CalendarIcon className="w-4 h-4" />
                        {new Date(rsvp.event_start_time).toLocaleDateString('en-US', {
                          weekday: 'short',
                          month: 'long',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </div>
                    )}

                    {rsvp.event_location && (
                      <div className="flex items-center gap-2 text-sm text-muted-foreground">
                        <MapPinIcon className="w-4 h-4" />
                        {rsvp.event_location}
                      </div>
                    )}
                  </div>

                  {rsvp.status === 'ATTENDING' && (
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDownload(rsvp.id)}
                    >
                      <Download className="w-4 h-4 mr-1" />
                      .ics
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
