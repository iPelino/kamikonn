import { useEffect } from 'react';
import { useInView } from 'react-intersection-observer';
import { useModerationQueue } from '../hooks/useModeration';
import { ModeratorEventCard } from '../components/ModeratorEventCard';
import { Loader2 } from 'lucide-react';

export function ModerationQueuePage() {
  const { data, isLoading, isError, fetchNextPage, hasNextPage, isFetchingNextPage } = useModerationQueue();
  const { ref, inView } = useInView();

  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, fetchNextPage]);

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-forest" />
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex h-64 items-center justify-center text-red-500">
        Error loading moderation queue. Are you a university moderator?
      </div>
    );
  }

  const events = data?.pages.flatMap((page) => page.results) || [];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold font-heading text-forest">Moderation Queue</h1>
        <p className="text-muted-foreground mt-2">
          Review and approve events submitted for your university.
        </p>
      </div>

      {events.length === 0 ? (
        <div className="text-center py-20 bg-muted/30 rounded-lg border border-dashed">
          <p className="text-muted-foreground">No pending events to review.</p>
        </div>
      ) : (
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {events.map((event) => (
            <ModeratorEventCard key={event.slug} event={event} />
          ))}
        </div>
      )}

      {/* Infinite scrolling trigger */}
      <div ref={ref} className="h-10 mt-6 flex items-center justify-center">
        {isFetchingNextPage && <Loader2 className="w-6 h-6 animate-spin text-forest" />}
      </div>
    </div>
  );
}
