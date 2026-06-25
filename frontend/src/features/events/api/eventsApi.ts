import apiClient from '@/api/client';
import type { Event, PaginatedResponse, Category } from '@/types/events';

export interface GetEventsParams {
  q?: string;
  category__slug?: string;
  universities__short_name?: string;
  is_virtual?: boolean;
  status?: string;
  start_date_after?: string;
  start_date_before?: string;
  cursor?: string;
}

export const getEvents = async (params?: GetEventsParams): Promise<PaginatedResponse<Event>> => {
  const { data } = await apiClient.get<PaginatedResponse<Event>>('/events/', { params });
  return data;
};

export const getEventBySlug = async (slug: string): Promise<Event> => {
  const { data } = await apiClient.get<Event>(`/events/${slug}/`);
  return data;
};

export const getCategories = async (): Promise<PaginatedResponse<Category>> => {
  const { data } = await apiClient.get<PaginatedResponse<Category>>('/categories/');
  return data;
};
