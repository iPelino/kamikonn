import { Routes, Route, Link } from 'react-router';
import PageContainer from './components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import { SEO } from './components/SEO';
import { lazy, Suspense } from 'react';

const LoginPage = lazy(() => import('./features/auth/pages/LoginPage'));
const RegisterPage = lazy(() => import('./features/auth/pages/RegisterPage'));
const VerifyEmailPage = lazy(() => import('./features/auth/pages/VerifyEmailPage'));
const EventDiscoveryPage = lazy(() => import('./features/events/pages/EventDiscoveryPage').then(module => ({ default: module.EventDiscoveryPage })));
const EventDetailPage = lazy(() => import('./features/events/pages/EventDetailPage').then(module => ({ default: module.EventDetailPage })));
const OrganizerProfilePage = lazy(() => import('./features/organizers/pages/OrganizerProfilePage').then(module => ({ default: module.OrganizerProfilePage })));
const OrganizerDashboardPage = lazy(() => import('./features/organizers/pages/OrganizerDashboardPage').then(module => ({ default: module.OrganizerDashboardPage })));
const BecomeOrganizerPage = lazy(() => import('./features/organizers/pages/BecomeOrganizerPage').then(module => ({ default: module.BecomeOrganizerPage })));
const ModerationQueuePage = lazy(() => import('./features/moderation/pages/ModerationQueuePage').then(module => ({ default: module.ModerationQueuePage })));
const CreateEventPage = lazy(() => import('./features/events/pages/CreateEventPage').then(module => ({ default: module.CreateEventPage })));
const UniversityManagementPage = lazy(() => import('./features/universities/pages/UniversityManagementPage').then(module => ({ default: module.UniversityManagementPage })));
const MyRSVPsPage = lazy(() => import('./features/rsvp/pages/MyRSVPsPage').then(module => ({ default: module.MyRSVPsPage })));

const PageLoader = () => (
  <div className="flex h-[50vh] items-center justify-center">
    <div className="h-8 w-8 animate-spin rounded-full border-4 border-forest border-t-transparent"></div>
  </div>
);

// Placeholder Home component
function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <SEO title="Home" />
      <h1 className="mb-6 font-heading text-4xl font-bold md:text-6xl">
        Discover Academic Events Across <span className="text-forest">Rwanda</span>
      </h1>
      <p className="mb-8 max-w-2xl text-lg text-charcoal/80">
        The central hub for academic seminars, hackathons, and workshops across Kigali's universities.
      </p>
      <div className="flex gap-4">
        <Link to="/events">
          <Button className="bg-amber text-forest hover:bg-amber/90" size="lg">Explore Events</Button>
        </Link>
        <Link to="/events/create">
          <Button variant="outline" className="border-forest text-forest hover:bg-forest/5" size="lg">
            Create Event
          </Button>
        </Link>
        <Link to="/organizer/become">
          <Button variant="outline" className="border-forest text-forest hover:bg-forest/5" size="lg">
            Become an Organizer
          </Button>
        </Link>
      </div>
    </div>
  );
}

function App() {
  return (
    <PageContainer>
      <SEO />
      <Suspense fallback={<PageLoader />}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/verify-email/:key" element={<VerifyEmailPage />} />
          <Route path="/events" element={<EventDiscoveryPage />} />
          <Route path="/events/create" element={<CreateEventPage />} />
          <Route path="/events/:slug" element={<EventDetailPage />} />
          <Route path="/organizer/become" element={<BecomeOrganizerPage />} />
          <Route path="/organizer/dashboard" element={<OrganizerDashboardPage />} />
          <Route path="/organizer/:id" element={<OrganizerProfilePage />} />
          <Route path="/moderation/queue" element={<ModerationQueuePage />} />
          <Route path="/admin/universities" element={<UniversityManagementPage />} />
          <Route path="/my-rsvps" element={<MyRSVPsPage />} />
        </Routes>
      </Suspense>
    </PageContainer>
  );
}

export default App;
