export interface OrganizerProfile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  bio: string;
  website: string;
  social_links: Record<string, string>;
  trust_tier: number;
  is_verified: boolean;
  successful_events_count: number;
}
