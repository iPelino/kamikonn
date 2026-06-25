import { useModerationLogs } from '../hooks/useModeration';
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

export function ModerationLogsTable() {
  const { data, isLoading, isError, hasNextPage, fetchNextPage, isFetchingNextPage } = useModerationLogs();

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-forest" />
      </div>
    );
  }

  if (isError) {
    return <div className="text-red-500 py-8 text-center">Failed to load moderation logs.</div>;
  }

  const logs = data?.pages.flatMap((page) => page.results) || [];

  if (logs.length === 0) {
    return (
      <div className="text-center py-20 bg-muted/30 rounded-lg border border-dashed">
        <p className="text-muted-foreground">No moderation logs found.</p>
      </div>
    );
  }

  const getActionVariant = (action: string) => {
    switch (action) {
      case 'APPROVED':
        return 'default';
      case 'REJECTED':
      case 'FLAGGED':
        return 'destructive';
      case 'FLAG_RESOLVED':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  return (
    <div className="space-y-4">
      <div className="rounded-md border bg-card overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Event</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Moderator</TableHead>
              <TableHead>Reason</TableHead>
              <TableHead className="text-right">Date</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {logs.map((log) => (
              <TableRow key={log.id}>
                <TableCell className="font-medium">{log.event_title}</TableCell>
                <TableCell>
                  <Badge variant={getActionVariant(log.action) as any}>
                    {log.action}
                  </Badge>
                </TableCell>
                <TableCell>{log.moderator_email || 'System / User'}</TableCell>
                <TableCell className="max-w-[200px] truncate" title={log.reason}>
                  {log.reason || '-'}
                </TableCell>
                <TableCell className="text-right">
                  {new Date(log.created_at).toLocaleString()}
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
