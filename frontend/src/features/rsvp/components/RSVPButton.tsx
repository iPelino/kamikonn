import { Link } from 'react-router';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, CalendarPlus, CalendarX2, Bookmark, BookmarkCheck, Download } from 'lucide-react';
import { useRSVP } from '../hooks/useRSVP';

interface RSVPButtonProps {
  eventSlug: string;
}

export function RSVPButton({ eventSlug }: RSVPButtonProps) {
  const {
    rsvp,
    savedEvent,
    isLoading,
    isAuthenticated,
    handleRSVP,
    handleCancel,
    handleSave,
    handleCalendar,
    isPending,
    isSavePending,
  } = useRSVP(eventSlug);

  if (!isAuthenticated) {
    return (
      <div className="space-y-3">
        <Link to="/login">
          <Button className="w-full" size="lg">
            Sign in to RSVP
          </Button>
        </Link>
        <p className="text-xs text-center text-muted-foreground">
          You need an account to register for events.
        </p>
      </div>
    );
  }

  if (isLoading) {
    return (
      <Button className="w-full" size="lg" disabled>
        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
        Loading...
      </Button>
    );
  }

  return (
    <div className="space-y-3">
      {/* RSVP Status Badge */}
      {rsvp && (
        <div className="flex justify-center">
          {rsvp.status === 'ATTENDING' && (
            <Badge className="bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-4 py-1.5 text-sm">
              You are attending
            </Badge>
          )}
          {rsvp.status === 'WAITLISTED' && (
            <Badge className="bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200 px-4 py-1.5 text-sm">
              You are on the waitlist
            </Badge>
          )}
        </div>
      )}

      {/* Primary RSVP / Cancel action */}
      {!rsvp ? (
        <Button
          className="w-full"
          size="lg"
          onClick={() => handleRSVP()}
          disabled={isPending}
        >
          {isPending ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <CalendarPlus className="mr-2 h-4 w-4" />
          )}
          RSVP Now
        </Button>
      ) : (
        <Button
          variant="destructive"
          className="w-full"
          size="lg"
          onClick={() => handleCancel()}
          disabled={isPending}
        >
          {isPending ? (
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          ) : (
            <CalendarX2 className="mr-2 h-4 w-4" />
          )}
          Cancel RSVP
        </Button>
      )}

      {/* Calendar download - only if attending */}
      {rsvp?.status === 'ATTENDING' && (
        <Button
          variant="outline"
          className="w-full"
          onClick={() => handleCalendar()}
        >
          <Download className="mr-2 h-4 w-4" />
          Add to Calendar (.ics)
        </Button>
      )}

      {/* Save / unsave */}
      <Button
        variant="ghost"
        className="w-full text-muted-foreground hover:text-foreground"
        onClick={() => handleSave()}
        disabled={isSavePending}
      >
        {savedEvent ? (
          <>
            <BookmarkCheck className="mr-2 h-4 w-4 text-primary" />
            Saved
          </>
        ) : (
          <>
            <Bookmark className="mr-2 h-4 w-4" />
            Save Event
          </>
        )}
      </Button>
    </div>
  );
}
