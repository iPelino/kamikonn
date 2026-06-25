import { useInfiniteQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getModerationQueue, approveEvent, rejectEvent, getFlagReports, resolveFlagReport, dismissFlagReport, getModerationLogs } from '../api/moderationApi';

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

export const useFlagReports = () => {
  return useInfiniteQuery({
    queryKey: ['flag-reports'],
    queryFn: ({ pageParam }) => getFlagReports(pageParam),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => {
      if (!lastPage.next) return undefined;
      const url = new URL(lastPage.next);
      return url.searchParams.get('cursor') || undefined;
    },
  });
};

export const useResolveFlag = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => resolveFlagReport(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flag-reports'] });
    },
  });
};

export const useDismissFlag = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => dismissFlagReport(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['flag-reports'] });
    },
  });
};

export const useModerationLogs = () => {
  return useInfiniteQuery({
    queryKey: ['moderation-logs'],
    queryFn: ({ pageParam }) => getModerationLogs(pageParam),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) => {
      if (!lastPage.next) return undefined;
      const url = new URL(lastPage.next);
      return url.searchParams.get('cursor') || undefined;
    },
  });
};
