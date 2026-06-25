import { useCurrentOrganizerProfile } from '../hooks/useOrganizers';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, DownloadIcon, UsersIcon, CalendarIcon, CheckCircle2Icon } from 'lucide-react';
import { CsvImportButton } from '../../events/components/CsvImportButton';

export function OrganizerDashboardPage() {
  const { data: profile, isLoading, isError } = useCurrentOrganizerProfile(true);

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
        <h2 className="text-2xl font-bold mb-4">Not an Organizer</h2>
        <p className="text-muted-foreground mb-8">You need to register as an organizer to access this dashboard.</p>
        <Button>Become an Organizer</Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Organizer Dashboard</h1>
          <p className="text-muted-foreground">Manage your events and track RSVPs</p>
        </div>
        <div className="flex gap-4">
          <CsvImportButton />
          <Button>
            Create New Event
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Events</CardTitle>
            <CalendarIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{profile.successful_events_count}</div>
            <p className="text-xs text-muted-foreground">Approved and completed</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total RSVPs</CardTitle>
            <UsersIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">--</div>
            <p className="text-xs text-muted-foreground">Across all your events</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Trust Tier</CardTitle>
            <CheckCircle2Icon className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">Tier {profile.trust_tier}</div>
            <p className="text-xs text-muted-foreground">
              {profile.is_verified ? "Verified Partner" : "Standard Organizer"}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold">Your Events</h2>
          <Button variant="outline" size="sm">
            <DownloadIcon className="w-4 h-4 mr-2" />
            Export All RSVPs (CSV)
          </Button>
        </div>

        <div className="bg-card border rounded-lg overflow-hidden">
          <div className="p-8 text-center text-muted-foreground">
            <p>You haven't created any events yet.</p>
            <Button variant="link" className="mt-2">Create your first event</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
