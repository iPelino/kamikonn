import { Link } from 'react-router';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Flag, Building2 } from 'lucide-react';
import { SEO } from '@/components/SEO';

export default function AdminDashboardPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <SEO title="Admin Dashboard" />
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold tracking-tight text-forest">
          Admin Dashboard
        </h1>
        <p className="mt-2 text-charcoal/70">
          Platform administration and moderation tools.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <Card className="border-red-200 shadow-sm transition-shadow hover:shadow-md">
          <CardHeader className="flex flex-row items-start gap-4 pb-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-red-50">
              <Flag className="h-5 w-5 text-red-600" />
            </div>
            <div className="flex-1">
              <CardTitle className="font-heading text-lg font-semibold">Flag Review Queue</CardTitle>
              <CardDescription className="mt-1 text-sm text-charcoal/60">
                Review and action flagged events awaiting moderation.
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-2">
            <Button
              asChild
              className="w-full bg-red-600 text-white hover:bg-red-700"
            >
              <Link to="/moderation/queue">Open Queue</Link>
            </Button>
          </CardContent>
        </Card>

        <Card className="border-forest/10 shadow-sm transition-shadow hover:shadow-md">
          <CardHeader className="flex flex-row items-start gap-4 pb-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-forest/10">
              <Building2 className="h-5 w-5 text-forest" />
            </div>
            <div className="flex-1">
              <CardTitle className="font-heading text-lg font-semibold">University Management</CardTitle>
              <CardDescription className="mt-1 text-sm text-charcoal/60">
                Create, edit, and manage university profiles and moderators.
              </CardDescription>
            </div>
          </CardHeader>
          <CardContent className="pt-2">
            <Button
              asChild
              variant="outline"
              className="w-full border-forest text-forest hover:bg-forest/5"
            >
              <Link to="/admin/universities">Manage Universities</Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
