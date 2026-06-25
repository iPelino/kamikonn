import apiClient from '@/api/client';
import type { Event, PaginatedResponse } from '@/types/events';
import type { FlagReport, ModerationLog } from '../types';

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

export const createFlagReport = async (eventId: number, reason: string): Promise<FlagReport> => {
  const { data } = await apiClient.post<FlagReport>('/moderation/flags/', {
    event: eventId,
    reason,
  });
  return data;
};

export const getFlagReports = async (cursor?: string): Promise<PaginatedResponse<FlagReport>> => {
  const { data } = await apiClient.get<PaginatedResponse<FlagReport>>('/moderation/flags/', {
    params: { cursor },
  });
  return data;
};

export const resolveFlagReport = async (id: number): Promise<{ status: string }> => {
  const { data } = await apiClient.post<{ status: string }>(`/moderation/flags/${id}/resolve/`);
  return data;
};

export const dismissFlagReport = async (id: number): Promise<{ status: string }> => {
  const { data } = await apiClient.post<{ status: string }>(`/moderation/flags/${id}/dismiss/`);
  return data;
};

export const getModerationLogs = async (cursor?: string): Promise<PaginatedResponse<ModerationLog>> => {
  const { data } = await apiClient.get<PaginatedResponse<ModerationLog>>('/moderation/logs/', {
    params: { cursor },
  });
  return data;
};
