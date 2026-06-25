import { Routes, Route, Link } from 'react-router';
import PageContainer from './components/layout/PageContainer';
import { Button } from '@/components/ui/button';
import LoginPage from './features/auth/pages/LoginPage';
import RegisterPage from './features/auth/pages/RegisterPage';
import VerifyEmailPage from './features/auth/pages/VerifyEmailPage';
import { EventDiscoveryPage } from './features/events/pages/EventDiscoveryPage';
import { EventDetailPage } from './features/events/pages/EventDetailPage';
import { OrganizerProfilePage } from './features/organizers/pages/OrganizerProfilePage';
import { OrganizerDashboardPage } from './features/organizers/pages/OrganizerDashboardPage';
import { BecomeOrganizerPage } from './features/organizers/pages/BecomeOrganizerPage';
import { ModerationQueuePage } from './features/moderation/pages/ModerationQueuePage';
import { CreateEventPage } from './features/events/pages/CreateEventPage';

// Placeholder Home component
function Home() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
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
      </Routes>
    </PageContainer>
  );
}

export default App;
