import { Routes, Route } from 'react-router';
import PageContainer from './components/layout/PageContainer';
import { SEO } from './components/SEO';
import { lazy, Suspense } from 'react';
import { PageSkeleton } from './components/skeletons/EventSkeletons';

// Auth pages
const LoginPage = lazy(() => import('./features/auth/pages/LoginPage'));
const RegisterPage = lazy(() => import('./features/auth/pages/RegisterPage'));
const VerifyEmailPage = lazy(() => import('./features/auth/pages/VerifyEmailPage'));

// Event pages
const EventDiscoveryPage = lazy(() =>
  import('./features/events/pages/EventDiscoveryPage').then((m) => ({ default: m.EventDiscoveryPage })),
);
const EventDetailPage = lazy(() =>
  import('./features/events/pages/EventDetailPage').then((m) => ({ default: m.EventDetailPage })),
);
const CreateEventPage = lazy(() =>
  import('./features/events/pages/CreateEventPage').then((m) => ({ default: m.CreateEventPage })),
);

// Organizer pages
const OrganizerProfilePage = lazy(() =>
  import('./features/organizers/pages/OrganizerProfilePage').then((m) => ({ default: m.OrganizerProfilePage })),
);
const OrganizerDashboardPage = lazy(() =>
  import('./features/organizers/pages/OrganizerDashboardPage').then((m) => ({ default: m.OrganizerDashboardPage })),
);
const BecomeOrganizerPage = lazy(() =>
  import('./features/organizers/pages/BecomeOrganizerPage').then((m) => ({ default: m.BecomeOrganizerPage })),
);

// Moderation + admin
const ModerationQueuePage = lazy(() =>
  import('./features/moderation/pages/ModerationQueuePage').then((m) => ({ default: m.ModerationQueuePage })),
);
const UniversityManagementPage = lazy(() =>
  import('./features/universities/pages/UniversityManagementPage').then((m) => ({ default: m.UniversityManagementPage })),
);

// User pages
const MyRSVPsPage = lazy(() =>
  import('./features/rsvp/pages/MyRSVPsPage').then((m) => ({ default: m.MyRSVPsPage })),
);

// New pages added in UX sprint
const LandingPage = lazy(() =>
  import('./features/home/LandingPage').then((m) => ({ default: m.LandingPage })),
);
const UserDashboardPage = lazy(() => import('./features/user/pages/UserDashboardPage'));
const SavedEventsPage = lazy(() => import('./features/user/pages/SavedEventsPage'));
const AdminDashboardPage = lazy(() => import('./features/admin/pages/AdminDashboardPage'));
const NotificationPreferencesPage = lazy(() => import('./features/user/pages/NotificationPreferencesPage'));
const UniversityProfilePage = lazy(() => import('./features/universities/pages/UniversityProfilePage'));

function App() {
  return (
    <PageContainer>
      <SEO />
      {/* PageSkeleton mirrors the content layout — no blank/spinner flash */}
      <Suspense fallback={<PageSkeleton />}>
        <Routes>
          {/* Home */}
          <Route path="/" element={<LandingPage />} />

          {/* Auth */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/verify-email/:key" element={<VerifyEmailPage />} />

          {/* Events */}
          <Route path="/events" element={<EventDiscoveryPage />} />
          <Route path="/events/create" element={<CreateEventPage />} />
          <Route path="/events/:slug" element={<EventDetailPage />} />

          {/* Organizer */}
          <Route path="/organizer/become" element={<BecomeOrganizerPage />} />
          <Route path="/organizer/dashboard" element={<OrganizerDashboardPage />} />
          <Route path="/organizer/:id" element={<OrganizerProfilePage />} />

          {/* Moderation + admin */}
          <Route path="/moderation/queue" element={<ModerationQueuePage />} />
          <Route path="/admin" element={<AdminDashboardPage />} />
          <Route path="/admin/universities" element={<UniversityManagementPage />} />

          {/* User account */}
          <Route path="/my-rsvps" element={<MyRSVPsPage />} />
          <Route path="/dashboard" element={<UserDashboardPage />} />
          <Route path="/saved-events" element={<SavedEventsPage />} />
          <Route path="/notifications/preferences" element={<NotificationPreferencesPage />} />

          {/* Universities */}
          <Route path="/universities/:slug" element={<UniversityProfilePage />} />
        </Routes>
      </Suspense>
    </PageContainer>
  );
}

export default App;
