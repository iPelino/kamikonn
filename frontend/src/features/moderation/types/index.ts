import type { Event } from '@/types/events';

export interface FlagReport {
  id: number;
  event: number;
  event_details: Event;
  reporter_email: string;
  reason: string;
  status: 'PENDING' | 'RESOLVED' | 'DISMISSED';
  created_at: string;
  updated_at: string;
}

export interface ModerationLog {
  id: number;
  event: number;
  event_title: string;
  moderator_email: string;
  action: 'APPROVED' | 'REJECTED' | 'FLAGGED' | 'FLAG_RESOLVED' | 'FLAG_DISMISSED';
  reason: string;
  created_at: string;
}
