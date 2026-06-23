import { ReactNode } from 'react';
import Header from './Header';
import Footer from './Footer';

interface PageContainerProps {
  children: ReactNode;
}

export default function PageContainer({ children }: PageContainerProps) {
  return (
    <div className="relative flex min-h-screen flex-col bg-sage text-charcoal">
      <Header />
      <main className="flex-1 w-full max-w-7xl mx-auto p-4 md:p-6 lg:p-8">
        {children}
      </main>
      <Footer />
    </div>
  );
}
