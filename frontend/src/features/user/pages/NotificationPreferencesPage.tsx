import { useState } from 'react';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { SEO } from '@/components/SEO';

interface NotificationSetting {
  id: string;
  label: string;
  description: string;
  defaultValue: boolean;
}

const NOTIFICATION_SETTINGS: NotificationSetting[] = [
  {
    id: 'rsvp-confirmation',
    label: 'RSVP confirmation emails',
    description: 'Receive an email whenever you register for an event.',
    defaultValue: true,
  },
  {
    id: 'event-reminders',
    label: '24-hour event reminders',
    description: 'Get a reminder email one day before events you have RSVPed to.',
    defaultValue: true,
  },
  {
    id: 'new-events-organizer',
    label: 'New events from followed organizers',
    description: 'Be notified when an organizer you follow publishes a new event.',
    defaultValue: false,
  },
  {
    id: 'event-updates',
    label: 'Event update notifications',
    description: 'Receive alerts when details change on events you are attending.',
    defaultValue: true,
  },
];

export default function NotificationPreferencesPage() {
  const [preferences, setPreferences] = useState<Record<string, boolean>>(
    () => Object.fromEntries(NOTIFICATION_SETTINGS.map((s) => [s.id, s.defaultValue]))
  );
  const [saved, setSaved] = useState(false);

  const handleToggle = (id: string, value: boolean) => {
    setPreferences((prev) => ({ ...prev, [id]: value }));
    setSaved(false);
  };

  const handleSave = () => {
    // TODO: wire up to PATCH /api/auth/profile/ or dedicated endpoint
    setSaved(true);
  };

  return (
    <div className="container mx-auto max-w-2xl px-4 py-8">
      <SEO title="Notification Preferences" />
      <div className="mb-8">
        <h1 className="font-heading text-3xl font-bold tracking-tight text-forest">
          Notification Preferences
        </h1>
        <p className="mt-2 text-charcoal/70">
          Choose which email notifications you want to receive.
        </p>
      </div>

      <Card className="border-forest/10 shadow-sm">
        <CardHeader className="pb-4">
          <CardTitle className="font-heading text-lg font-semibold">Email Notifications</CardTitle>
          <CardDescription className="text-charcoal/60">
            These settings control which automated emails KamiKonn sends you.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {NOTIFICATION_SETTINGS.map((setting) => (
              <div
                key={setting.id}
                className="flex items-start justify-between gap-4"
              >
                <div className="flex-1 space-y-0.5">
                  <Label
                    htmlFor={setting.id}
                    className="text-sm font-medium leading-none text-charcoal"
                  >
                    {setting.label}
                  </Label>
                  <p className="text-xs text-charcoal/60">{setting.description}</p>
                </div>
                <Switch
                  id={setting.id}
                  checked={preferences[setting.id]}
                  onCheckedChange={(value: boolean) => handleToggle(setting.id, value)}
                />
              </div>
            ))}
          </div>

          <div className="mt-8 flex items-center gap-4">
            <Button
              onClick={handleSave}
              className="bg-forest text-white hover:bg-forest/90"
            >
              Save Preferences
            </Button>
            {saved && (
              <p className="text-sm text-green-600 dark:text-green-400">
                Preferences saved.
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
