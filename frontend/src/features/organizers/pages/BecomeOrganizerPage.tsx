import { useState } from 'react';
import { useNavigate } from 'react-router';
import { useBecomeOrganizer } from '../hooks/useOrganizers';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
import { Loader2 } from 'lucide-react';

export function BecomeOrganizerPage() {
  const [bio, setBio] = useState('');
  const [website, setWebsite] = useState('');
  const navigate = useNavigate();
  const { mutate: becomeOrganizer, isPending, error } = useBecomeOrganizer();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    becomeOrganizer(
      { bio, website },
      {
        onSuccess: () => {
          navigate('/organizer/dashboard');
        },
      }
    );
  };

  return (
    <div className="container mx-auto px-4 py-12 max-w-lg">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Become an Organizer</CardTitle>
          <CardDescription>
            Join KamiKonn as an event organizer. You'll be able to publish events, manage RSVPs, and build your community.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form id="become-organizer-form" onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="bio">Bio</Label>
              <Input
                id="bio"
                placeholder="Tell us about yourself or your organization..."
                value={bio}
                onChange={(e) => setBio(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="website">Website (Optional)</Label>
              <Input
                id="website"
                type="url"
                placeholder="https://example.com"
                value={website}
                onChange={(e) => setWebsite(e.target.value)}
              />
            </div>

            {error && (
              <div className="text-sm text-destructive">
                {error.message || 'Failed to register as organizer. Please try again.'}
              </div>
            )}
          </form>
        </CardContent>
        <CardFooter>
          <Button
            type="submit"
            form="become-organizer-form"
            className="w-full"
            disabled={isPending}
          >
            {isPending ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Submitting...
              </>
            ) : (
              'Submit Application'
            )}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
