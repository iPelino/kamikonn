export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
  icon: string;
}

export interface University {
  id: string;
  name: string;
  short_name: string;
  domain: string;
}

export interface Organizer {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Event {
  id: string;
  title: string;
  slug: string;
  description: string;
  start_time: string;
  end_time: string;
  location: string;
  is_virtual: boolean;
  virtual_link: string;
  banner_image: string | null;
  status: string;
  capacity: number;
  price: string;
  payment_link: string;
  organizer: Organizer;
  category: Category | null;
  universities: University[];
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}
