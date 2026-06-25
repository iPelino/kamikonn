import apiClient from '@/api/client';

export interface Moderator {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}

export interface University {
  id: string;
  name: string;
  short_name: string;
  domain: string;
  logo_url: string;
  is_active: boolean;
  moderators: Moderator[];
  created_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export const fetchUniversities = async (): Promise<University[]> => {
  const response = await apiClient.get<PaginatedResponse<University>>('/universities/');
  return response.data.results;
};

export const createUniversity = async (data: Partial<University>): Promise<University> => {
  const response = await apiClient.post<University>('/universities/', data);
  return response.data;
};

export const updateUniversity = async (id: string, data: Partial<University>): Promise<University> => {
  const response = await apiClient.patch<University>(`/universities/${id}/`, data);
  return response.data;
};

export const assignModerator = async (universityId: string, userId: number): Promise<void> => {
  await apiClient.post(`/universities/${universityId}/assign_moderator/`, { user_id: userId });
};

export const removeModerator = async (universityId: string, userId: number): Promise<void> => {
  await apiClient.post(`/universities/${universityId}/remove_moderator/`, { user_id: userId });
};
