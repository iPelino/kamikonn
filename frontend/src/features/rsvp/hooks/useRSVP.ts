import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getMyRSVP,
  createRSVP,
  cancelRSVP,
  getMySavedEvent,
  saveEvent,
  unsaveEvent,
  downloadCalendar,
} from '../api/rsvpApi';
import { toast } from 'sonner';
import { useAuthStore } from '@/stores/authStore';

export function useRSVP(eventSlug: string) {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  const enabled = !!user && !!eventSlug;

  const { data: rsvp, isLoading: rsvpLoading } = useQuery({
    queryKey: ['rsvp', eventSlug],
    queryFn: () => getMyRSVP(eventSlug),
    enabled,
  });

  const { data: savedEvent, isLoading: savedLoading } = useQuery({
    queryKey: ['saved-event', eventSlug],
    queryFn: () => getMySavedEvent(eventSlug),
    enabled,
  });

  const rsvpMutation = useMutation({
    mutationFn: () => createRSVP(eventSlug),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['rsvp', eventSlug] });
      if (data.status === 'WAITLISTED') {
        toast.success("You have been added to the waitlist. We will notify you if a spot opens up.");
      } else {
        toast.success("You are now registered for this event!");
      }
    },
    onError: () => toast.error('Failed to RSVP. Please try again.'),
  });

  const cancelMutation = useMutation({
    mutationFn: () => cancelRSVP(eventSlug),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['rsvp', eventSlug] });
      toast.success('Your RSVP has been cancelled.');
    },
    onError: () => toast.error('Failed to cancel RSVP.'),
  });

  const saveMutation = useMutation<void, Error, void>({
    mutationFn: async () => {
      if (savedEvent) {
        await unsaveEvent(eventSlug);
      } else {
        await saveEvent(eventSlug);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-event', eventSlug] });
      toast.success(savedEvent ? 'Event removed from saved.' : 'Event saved!');
    },
    onError: () => toast.error('Failed to update saved events.'),
  });

  const calendarMutation = useMutation({
    mutationFn: () => downloadCalendar(eventSlug),
    onSuccess: () => toast.success('Calendar file downloaded.'),
    onError: () => toast.error('Failed to download calendar.'),
  });

  return {
    rsvp,
    savedEvent,
    isLoading: rsvpLoading || savedLoading,
    isAuthenticated: !!user,
    handleRSVP: rsvpMutation.mutate,
    handleCancel: cancelMutation.mutate,
    handleSave: saveMutation.mutate,
    handleCalendar: calendarMutation.mutate,
    isPending: rsvpMutation.isPending || cancelMutation.isPending,
    isSavePending: saveMutation.isPending,
  };
}
