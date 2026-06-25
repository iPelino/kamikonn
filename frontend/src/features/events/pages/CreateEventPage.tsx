import { EventWizard } from '../components/wizard/EventWizard';

export function CreateEventPage() {
  return (
    <div className="container max-w-4xl py-10">
      <div className="mb-8 space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Create an Event</h1>
        <p className="text-muted-foreground">
          Fill out the details below to create a new academic event. It will be saved as a draft.
        </p>
      </div>

      <EventWizard />
    </div>
  );
}
