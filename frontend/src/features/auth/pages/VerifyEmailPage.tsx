import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import apiClient from '@/api/client';

export default function VerifyEmailPage() {
  const { key } = useParams<{ key: string }>();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');

  useEffect(() => {
    if (!key) {
      setStatus('error');
      return;
    }

    const verifyEmail = async () => {
      try {
        await apiClient.post('/auth/registration/verify-email/', { key });
        setStatus('success');
      } catch (err) {
        console.error('Email verification error', err);
        setStatus('error');
      }
    };

    verifyEmail();
  }, [key]);

  return (
    <div className="flex min-h-[60vh] items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-bold font-heading">Email Verification</CardTitle>
          <CardDescription>
            {status === 'verifying' && 'Verifying your email address...'}
            {status === 'success' && 'Your email has been verified!'}
            {status === 'error' && 'Verification failed. The link may be invalid or expired.'}
          </CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col items-center">
          {status === 'success' && (
            <Button className="w-full bg-forest hover:bg-forest/90 mt-4" onClick={() => navigate('/login')}>
              Go to Login
            </Button>
          )}
          {status === 'error' && (
            <Button className="w-full mt-4" variant="outline" onClick={() => navigate('/login')}>
              Return to Login
            </Button>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
