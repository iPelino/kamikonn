import apiClient from '@/api/client';
import type { Event, PaginatedResponse } from '@/types/events';

export const getModerationQueue = async (cursor?: string): Promise<PaginatedResponse<Event>> => {
  const { data } = await apiClient.get<PaginatedResponse<Event>>('/moderation/events/', {
    params: { cursor },
  });
  return data;
};

export const approveEvent = async (slug: string): Promise<{ status: string; event: string }> => {
  const { data } = await apiClient.post<{ status: string; event: string }>(`/moderation/events/${slug}/approve/`);
  return data;
};

export const rejectEvent = async (slug: string): Promise<{ status: string; event: string }> => {
  const { data } = await apiClient.post<{ status: string; event: string }>(`/moderation/events/${slug}/reject/`);
  return data;
};
