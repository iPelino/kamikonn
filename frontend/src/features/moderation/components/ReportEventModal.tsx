import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { FlagIcon, Loader2 } from 'lucide-react';
import { toast } from 'sonner';

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { createFlagReport } from '../api/moderationApi';

interface ReportEventModalProps {
  eventId: string | number;
}

export function ReportEventModal({ eventId }: ReportEventModalProps) {
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState('');

  const { mutate, isPending } = useMutation({
    mutationFn: () => createFlagReport(Number(eventId), reason),
    onSuccess: () => {
      toast.success('Event reported successfully. Moderators will review it soon.');
      setOpen(false);
      setReason('');
    },
    onError: () => {
      toast.error('Failed to report event. Please try again.');
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!reason.trim()) {
      toast.error('Please provide a reason for reporting.');
      return;
    }
    mutate();
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-red-50 hover:text-red-500 h-8 px-3 text-muted-foreground">
        <FlagIcon className="w-4 h-4 mr-2" />
        Report Event
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Report Event</DialogTitle>
          <DialogDescription>
            If you believe this event violates our community guidelines (e.g., spam, inappropriate content, fake event), please report it to our moderators.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 pt-4">
          <div className="space-y-2">
            <label htmlFor="reason" className="text-sm font-medium">
              Reason for reporting
            </label>
            <Textarea
              id="reason"
              placeholder="Please provide details about why you are reporting this event..."
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              className="min-h-[100px]"
              required
            />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={isPending}>
              Cancel
            </Button>
            <Button type="submit" variant="destructive" disabled={isPending || !reason.trim()}>
              {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Submit Report
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
