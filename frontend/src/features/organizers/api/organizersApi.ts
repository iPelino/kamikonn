import apiClient from '@/api/client';
import type { OrganizerProfile } from '@/types/organizers';

export const getOrganizerProfile = async (userId: number): Promise<OrganizerProfile> => {
  const { data } = await apiClient.get<OrganizerProfile>(`/organizers/${userId}/`);
  return data;
};

export const becomeOrganizer = async (payload: { bio?: string; website?: string; social_links?: Record<string, string> }): Promise<OrganizerProfile> => {
  const { data } = await apiClient.post<OrganizerProfile>('/organizers/become/', payload);
  return data;
};

export const getCurrentOrganizerProfile = async (): Promise<OrganizerProfile> => {
  const { data } = await apiClient.get<OrganizerProfile>('/organizers/me/');
  return data;
};
