import { useFlagReports, useResolveFlag, useDismissFlag } from '../hooks/useModeration';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

export function FlagReportsTable() {
  const { data, isLoading, isError, hasNextPage, fetchNextPage, isFetchingNextPage } = useFlagReports();
  const { mutate: resolveFlag, isPending: isResolving } = useResolveFlag();
  const { mutate: dismissFlag, isPending: isDismissing } = useDismissFlag();

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-forest" />
      </div>
    );
  }

  if (isError) {
    return <div className="text-red-500 py-8 text-center">Failed to load flag reports.</div>;
  }

  const flags = data?.pages.flatMap((page) => page.results) || [];

  if (flags.length === 0) {
    return (
      <div className="text-center py-20 bg-muted/30 rounded-lg border border-dashed">
        <p className="text-muted-foreground">No flag reports pending.</p>
      </div>
    );
  }

  const handleResolve = (id: number) => {
    resolveFlag(id, {
      onSuccess: () => toast.success('Flag resolved successfully.'),
      onError: () => toast.error('Failed to resolve flag.'),
    });
  };

  const handleDismiss = (id: number) => {
    dismissFlag(id, {
      onSuccess: () => toast.success('Flag dismissed successfully.'),
      onError: () => toast.error('Failed to dismiss flag.'),
    });
  };

  return (
    <div className="space-y-4">
      <div className="rounded-md border bg-card overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Event</TableHead>
              <TableHead>Reporter</TableHead>
              <TableHead>Reason</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Date</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {flags.map((flag) => (
              <TableRow key={flag.id}>
                <TableCell className="font-medium">{flag.event_details?.title || 'Unknown Event'}</TableCell>
                <TableCell>{flag.reporter_email}</TableCell>
                <TableCell className="max-w-[200px] truncate" title={flag.reason}>
                  {flag.reason}
                </TableCell>
                <TableCell>
                  <Badge variant={flag.status === 'PENDING' ? 'destructive' : 'secondary'}>
                    {flag.status}
                  </Badge>
                </TableCell>
                <TableCell>{new Date(flag.created_at).toLocaleDateString()}</TableCell>
                <TableCell className="text-right space-x-2">
                  {flag.status === 'PENDING' && (
                    <>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleResolve(flag.id)}
                        disabled={isResolving || isDismissing}
                      >
                        Resolve
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-muted-foreground"
                        onClick={() => handleDismiss(flag.id)}
                        disabled={isResolving || isDismissing}
                      >
                        Dismiss
                      </Button>
                    </>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      {hasNextPage && (
        <div className="flex justify-center pt-4">
          <Button
            variant="outline"
            onClick={() => fetchNextPage()}
            disabled={isFetchingNextPage}
          >
            {isFetchingNextPage ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : 'Load More'}
          </Button>
        </div>
      )}
    </div>
  );
}
