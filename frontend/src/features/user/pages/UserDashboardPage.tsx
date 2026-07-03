import { Link } from 'react-router';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { CalendarCheck, Bookmark } from 'lucide-react';
import { SEO } from '@/components/SEO';

export default function UserDashboardPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <SEO title="My Dashboard" />
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold tracking-tight text-forest">
          My Dashboard
        </h1>
        <p className="mt-2 text-charcoal/70">
          Welcome back. Manage your events and preferences.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card className="border-forest/10 shadow-sm transition-shadow hover:shadow-md">
          <CardHeader className="flex flex-row items-start gap-4 pb-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-forest/10">
              <CalendarCheck className="h-5 w-5 text-forest" />
            </div>
            <div className="flex-1">
              <CardTitle className="font-heading text-lg font-semibold">My RSVPs</CardTitle>
              <CardDescription className="mt-1 text-sm text-charcoal/60">
                Events you have registered to attend.
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-2">
            <Button
              asChild
              className="w-full bg-forest text-white hover:bg-forest/90"
            >
              <Link to="/my-rsvps">View RSVPs</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="border-forest/10 shadow-sm transition-shadow hover:shadow-md">
          <CardHeader className="flex flex-row items-start gap-4 pb-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-amber/20">
              <Bookmark className="h-5 w-5 text-amber-700" />
            </div>
            <div className="flex-1">
              <CardTitle className="font-heading text-lg font-semibold">Saved Events</CardTitle>
              <CardDescription className="mt-1 text-sm text-charcoal/60">
                Events you have bookmarked for later.
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-2">
            <Button
              asChild
              variant="outline"
              className="w-full border-forest text-forest hover:bg-forest/5"
            >
              <Link to="/saved-events">View Saved</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
