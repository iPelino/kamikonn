import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getOrganizerProfile, becomeOrganizer, getCurrentOrganizerProfile } from '../api/organizersApi';
// Removed unused type import

export const useOrganizerProfile = (userId: number) => {
  return useQuery({
    queryKey: ['organizer', userId],
    queryFn: () => getOrganizerProfile(userId),
    enabled: !!userId,
  });
};

export const useCurrentOrganizerProfile = (enabled = false) => {
  return useQuery({
    queryKey: ['organizer', 'me'],
    queryFn: getCurrentOrganizerProfile,
    enabled,
    retry: 1,
  });
};

export const useBecomeOrganizer = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: becomeOrganizer,
    onSuccess: (data) => {
      queryClient.setQueryData(['organizer', 'me'], data);
    },
  });
};
