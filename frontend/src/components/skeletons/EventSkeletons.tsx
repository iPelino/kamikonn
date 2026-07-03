import { Skeleton } from '@/components/ui/skeleton';

/**
 * EventCard skeleton — mirrors the 2:1 image + 3-row content layout.
 * Use inside a grid whenever events are loading.
 */
export function EventCardSkeleton() {
  return (
    <div className="rounded-lg overflow-hidden border bg-card flex flex-col h-full animate-pulse">
      {/* Banner */}
      <Skeleton className="aspect-[2/1] w-full rounded-none" />

      <div className="p-4 flex-grow space-y-3">
        {/* Title */}
        <Skeleton className="h-5 w-3/4" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-2/3" />
      </div>

      <div className="p-4 pt-0 space-y-2">
        {/* Date */}
        <div className="flex items-center gap-2">
          <Skeleton className="h-4 w-4 rounded-full shrink-0" />
          <Skeleton className="h-4 w-40" />
        </div>
        {/* Location */}
        <div className="flex items-center gap-2">
          <Skeleton className="h-4 w-4 rounded-full shrink-0" />
          <Skeleton className="h-4 w-32" />
        </div>
      </div>

      <div className="p-4 pt-0 flex items-center justify-between">
        <Skeleton className="h-5 w-12" />
        <Skeleton className="h-4 w-24" />
      </div>
    </div>
  );
}

/**
 * Grid of EventCard skeletons — drop-in replacement while events load.
 */
export function EventGridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, i) => (
        <EventCardSkeleton key={i} />
      ))}
    </div>
  );
}

/**
 * Full-page loader skeleton — used by the Suspense fallback in App.tsx.
 * Renders a header bar + content placeholder so there is no blank screen.
 */
export function PageSkeleton() {
  return (
    <div className="w-full max-w-7xl mx-auto p-4 md:p-6 lg:p-8 space-y-8 animate-pulse">
      {/* Page heading */}
      <div className="space-y-2">
        <Skeleton className="h-8 w-48" />
        <Skeleton className="h-5 w-72" />
      </div>

      {/* Content grid */}
      <EventGridSkeleton count={6} />
    </div>
  );
}
