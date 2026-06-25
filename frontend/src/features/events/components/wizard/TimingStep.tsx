import { UseFormReturn } from 'react-hook-form';
import { EventFormData } from './EventWizard';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function TimingStep({ form }: { form: UseFormReturn<EventFormData> }) {
  const { register, formState: { errors } } = form;

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="start_time">Start Time</Label>
        <Input
          id="start_time"
          type="datetime-local"
          {...register('start_time')}
        />
        {errors.start_time && <p className="text-sm text-red-500">{errors.start_time.message}</p>}
        <p className="text-sm text-muted-foreground">When does the event begin?</p>
      </div>

      <div className="space-y-2">
        <Label htmlFor="end_time">End Time</Label>
        <Input
          id="end_time"
          type="datetime-local"
          {...register('end_time')}
        />
        {errors.end_time && <p className="text-sm text-red-500">{errors.end_time.message}</p>}
        <p className="text-sm text-muted-foreground">When does the event end?</p>
      </div>
    </div>
  );
}
