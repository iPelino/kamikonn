import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router';
import { useEvents, useCategories } from '../hooks/useEvents';
import { EventCard } from '../components/EventCard';
import { useDebounce } from '@/hooks/useDebounce';
import { Input } from '@/components/ui/input';
import { SearchIcon, SlidersHorizontal, Loader2 } from 'lucide-react';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export function EventDiscoveryPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const initialSearch = searchParams.get('q') || '';

  const [searchTerm, setSearchTerm] = useState(initialSearch);
  const debouncedSearch = useDebounce(searchTerm, 500);

  const { data: categoriesData } = useCategories();

  // Convert URL search params to an object for API
  const currentParams = Object.fromEntries(searchParams.entries());

  const { data: eventsData, isLoading, isError } = useEvents(currentParams);

  // Update URL when debounced search changes
  useEffect(() => {
    if (debouncedSearch) {
      searchParams.set('q', debouncedSearch);
    } else {
      searchParams.delete('q');
    }
    setSearchParams(searchParams);
  }, [debouncedSearch, setSearchParams, searchParams]);

  const handleFilterChange = (key: string, value: string | boolean | null) => {
    if (value) {
      searchParams.set(key, String(value));
    } else {
      searchParams.delete(key);
    }
    setSearchParams(searchParams);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <h1 className="text-3xl font-bold tracking-tight">Discover Events</h1>

        <div className="relative w-full md:w-96">
          <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search events by title, description..."
            className="pl-9"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-8">
        {/* Filter Sidebar */}
        <aside className="w-full md:w-64 shrink-0 space-y-6">
          <div className="flex items-center gap-2 font-semibold pb-2 border-b">
            <SlidersHorizontal className="h-4 w-4" />
            <h2>Filters</h2>
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <Label>Category</Label>
              <Select
                value={searchParams.get('category__slug') || 'all'}
                onValueChange={(val: string | null) => handleFilterChange('category__slug', val === 'all' ? null : val)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="All Categories" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {categoriesData?.results.map((cat) => (
                    <SelectItem key={cat.id} value={cat.slug}>{cat.name}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Format</Label>
              <div className="flex items-center space-x-2 pt-1">
                <Checkbox
                  id="virtual-only"
                  checked={searchParams.get('is_virtual') === 'true'}
                  onCheckedChange={(checked: boolean | 'indeterminate') => handleFilterChange('is_virtual', checked === true ? 'true' : null)}
                />
                <label
                  htmlFor="virtual-only"
                  className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                >
                  Virtual events only
                </label>
              </div>
            </div>

            <div className="space-y-2">
              <Label>Status</Label>
              <Select
                value={searchParams.get('status') || 'APPROVED'}
                onValueChange={(val: string | null) => handleFilterChange('status', val)}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="APPROVED">Upcoming</SelectItem>
                  <SelectItem value="DRAFT">My Drafts</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </aside>

        {/* Main Feed */}
        <main className="flex-1">
          {isLoading ? (
            <div className="flex justify-center items-center h-64">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
            </div>
          ) : isError ? (
            <div className="text-center text-destructive py-12">
              Failed to load events. Please try again later.
            </div>
          ) : !eventsData || eventsData.results.length === 0 ? (
            <div className="text-center text-muted-foreground py-12 bg-muted/30 rounded-lg border border-dashed">
              No events found matching your criteria.
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {eventsData.results.map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
