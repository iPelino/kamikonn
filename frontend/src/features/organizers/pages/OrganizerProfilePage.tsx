import { useParams } from 'react-router';
import { useOrganizerProfile } from '../hooks/useOrganizers';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, GlobeIcon, UserPlusIcon } from 'lucide-react';

export function OrganizerProfilePage() {
  const { id } = useParams<{ id: string }>();
  const { data: profile, isLoading, isError } = useOrganizerProfile(Number(id));

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (isError || !profile) {
    return (
      <div className="container mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold mb-4">Organizer Not Found</h2>
        <p className="text-muted-foreground">This organizer profile does not exist.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      <div className="bg-card rounded-2xl shadow-sm border overflow-hidden">
        {/* Cover Image Placeholder */}
        <div className="h-32 md:h-48 bg-gradient-to-r from-primary/20 to-primary/10"></div>

        <div className="px-6 sm:px-10 pb-10">
          <div className="flex flex-col sm:flex-row justify-between items-start gap-4 -mt-12 sm:-mt-16 mb-6">
            <div className="h-24 w-24 sm:h-32 sm:w-32 rounded-full border-4 border-background bg-muted flex items-center justify-center text-4xl font-bold text-muted-foreground">
              {profile.first_name?.[0] || profile.email[0].toUpperCase()}
            </div>

            <div className="pt-2 sm:pt-16 flex gap-3">
              <Button>
                <UserPlusIcon className="w-4 h-4 mr-2" />
                Follow
              </Button>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h1 className="text-3xl font-bold flex items-center gap-2">
                {profile.first_name} {profile.last_name}
                {profile.is_verified && (
                  <Badge variant="default" className="bg-blue-500 hover:bg-blue-600">Verified</Badge>
                )}
              </h1>
              <p className="text-muted-foreground">{profile.email}</p>
            </div>

            <div className="flex flex-wrap gap-4 text-sm text-muted-foreground">
              {profile.trust_tier > 1 && (
                <div className="flex items-center gap-1">
                  <Badge variant="secondary">Tier {profile.trust_tier} Organizer</Badge>
                </div>
              )}
              {profile.website && (
                <a href={profile.website} target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-primary transition-colors">
                  <GlobeIcon className="w-4 h-4" />
                  Website
                </a>
              )}
            </div>

            <div className="prose prose-sm dark:prose-invert max-w-none pt-4">
              <p>{profile.bio || "This organizer hasn't added a bio yet."}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-6">Upcoming Events</h2>
        {/* This would be a list of EventCards filtered by this organizer */}
        <div className="text-center py-12 border border-dashed rounded-xl text-muted-foreground">
          Events by this organizer will appear here.
        </div>
      </div>
    </div>
  );
}
