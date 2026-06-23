import { Routes, Route } from 'react-router';
import PageContainer from './components/layout/PageContainer';
import { Button } from '@/components/ui/button';

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
        <Button className="bg-amber text-forest hover:bg-amber/90" size="lg">
          Explore Events
        </Button>
        <Button variant="outline" className="border-forest text-forest hover:bg-forest/5" size="lg">
          Become an Organizer
        </Button>
      </div>
    </div>
  );
}

function App() {
  return (
    <PageContainer>
      <Routes>
        <Route path="/" element={<Home />} />
        {/* Other routes will be added here */}
      </Routes>
    </PageContainer>
  );
}

export default App;
