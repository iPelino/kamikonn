import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string;
  image?: string;
  url?: string;
}

export function SEO({
  title = 'KamiKonn - Academic Events in Kigali',
  description = 'Discover and RSVP to academic events across major universities in Kigali, Rwanda.',
  keywords = 'events, academic, Kigali, universities, Rwanda, students, RSVP',
  image = '/logo.png', // Fallback image
  url = 'https://kamikonn.com',
}: SEOProps) {
  const fullTitle = title === 'KamiKonn - Academic Events in Kigali' ? title : `${title} | KamiKonn`;

  return (
    <Helmet>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />

      {/* Open Graph / Facebook */}
      <meta property="og:type" content="website" />
      <meta property="og:url" content={url} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />

      {/* Twitter */}
      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:url" content={url} />
      <meta property="twitter:title" content={fullTitle} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={image} />
    </Helmet>
  );
}
