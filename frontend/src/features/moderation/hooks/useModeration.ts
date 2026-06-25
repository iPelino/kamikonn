import { useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getModerationQueue, approveEvent, rejectEvent } from '../api/moderationApi';

export const useModerationQueue = () => {
  return useInfiniteQuery({
    queryKey: ['moderation-queue'],
    queryFn: ({ pageParam }) => getModerationQueue(pageParam),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => {
      if (!lastPage.next) return undefined;
      const url = new URL(lastPage.next);
      return url.searchParams.get('cursor') || undefined;
    },
  });
};

export const useApproveEvent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (slug: string) => approveEvent(slug),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['moderation-queue'] });
    },
  });
};

export const useRejectEvent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (slug: string) => rejectEvent(slug),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['moderation-queue'] });
    },
  });
};
