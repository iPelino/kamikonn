import { useQuery } from '@tanstack/react-query';
import { getEvents, getEventBySlug, getCategories } from '../api/eventsApi';
import type { GetEventsParams } from '../api/eventsApi';

export const useEvents = (params: GetEventsParams = {}) => {
  return useQuery({
    queryKey: ['events', params],
    queryFn: () => getEvents(params),
  });
};

export const useEventDetails = (slug: string) => {
  return useQuery({
    queryKey: ['event', slug],
    queryFn: () => getEventBySlug(slug),
    enabled: !!slug,
  });
};

export const useCategories = () => {
  return useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
  });
};
