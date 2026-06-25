import apiClient from '@/api/client';

export type RSVPStatus = 'ATTENDING' | 'WAITLISTED' | 'CANCELLED';

export interface RSVP {
  id: string;
  event: string;
  event_title?: string;
  event_slug?: string;
  event_start_time?: string;
  event_location?: string;
  status: RSVPStatus;
  created_at: string;
}

export interface SavedEvent {
  id: string;
  event: string;
  created_at: string;
}

// RSVP to an event (by slug)
export const createRSVP = async (eventSlug: string): Promise<RSVP> => {
  const res = await apiClient.post<RSVP>(`/events/${eventSlug}/rsvp/`);
  return res.data;
};

// Cancel an RSVP (by slug)
export const cancelRSVP = async (eventSlug: string): Promise<void> => {
  await apiClient.delete(`/events/${eventSlug}/rsvp/`);
};

// Check current user's RSVP status for a specific event (by slug)
export const getMyRSVP = async (eventSlug: string): Promise<RSVP | null> => {
  try {
    const res = await apiClient.get<RSVP>(`/events/${eventSlug}/rsvp/`);
    return res.data;
  } catch {
    return null;
  }
};

// Download ICS calendar file (by slug)
export const downloadCalendar = async (eventSlug: string): Promise<void> => {
  const res = await apiClient.get(`/events/${eventSlug}/rsvp/calendar/`, {
    responseType: 'blob',
  });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'event.ics');
  document.body.appendChild(link);
  link.click();
  link.remove();
};

// Save an event (by slug)
export const saveEvent = async (eventSlug: string): Promise<SavedEvent> => {
  const res = await apiClient.post<SavedEvent>(`/events/${eventSlug}/save/`);
  return res.data;
};

// Unsave an event (by slug)
export const unsaveEvent = async (eventSlug: string): Promise<void> => {
  await apiClient.delete(`/events/${eventSlug}/save/`);
};

// Check if event is saved (by slug)
export const getMySavedEvent = async (eventSlug: string): Promise<SavedEvent | null> => {
  try {
    const res = await apiClient.get<SavedEvent>(`/events/${eventSlug}/save/`);
    return res.data;
  } catch {
    return null;
  }
};

// List all my RSVPs
export const listMyRSVPs = async (): Promise<RSVP[]> => {
  const res = await apiClient.get<{ results: RSVP[] } | RSVP[]>('/rsvps/my/');
  if (Array.isArray(res.data)) return res.data;
  return (res.data as { results: RSVP[] }).results ?? [];
};
