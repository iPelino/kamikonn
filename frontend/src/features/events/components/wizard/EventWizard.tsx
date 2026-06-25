import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { BasicInfoStep } from './BasicInfoStep';
import { TimingStep } from './TimingStep';
import { MediaStep } from './MediaStep';
import { apiClient } from '@/api/client';
import { toast } from 'sonner';
import { useNavigate } from 'react-router';

const eventSchema = z.object({
  title: z.string().min(3, "Title must be at least 3 characters").max(100),
  description: z.string().min(10, "Description must be at least 10 characters").optional().or(z.literal('')),
  category: z.string().optional().or(z.literal('')),
  is_virtual: z.boolean().default(false),
  location: z.string().optional().or(z.literal('')),
  start_time: z.string().optional().or(z.literal('')),
  end_time: z.string().optional().or(z.literal('')),
  banner_image: z.any().optional()
});

export type EventFormData = z.infer<typeof eventSchema>;

export function EventWizard() {
  const [step, setStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const form = useForm<EventFormData>({
    resolver: zodResolver(eventSchema),
    defaultValues: {
      title: '',
      description: '',
      category: '',
      is_virtual: false,
      location: '',
      start_time: '',
      end_time: ''
    }
  });

  const nextStep = async () => {
    let isValid = false;
    if (step === 1) {
      isValid = await form.trigger(['title', 'description', 'category', 'is_virtual', 'location']);
    } else if (step === 2) {
      isValid = await form.trigger(['start_time', 'end_time']);
    }

    if (isValid) {
      setStep(s => s + 1);
    }
  };

  const prevStep = () => {
    setStep(s => s - 1);
  };

  const onSubmit = async (data: EventFormData) => {
    setIsSubmitting(true);
    try {
      const formData = new FormData();
      formData.append('title', data.title);
      if (data.description) formData.append('description', data.description);
      if (data.category) formData.append('category', data.category);
      formData.append('is_virtual', String(data.is_virtual));
      if (data.location) formData.append('location', data.location);
      if (data.start_time) formData.append('start_time', new Date(data.start_time).toISOString());
      if (data.end_time) formData.append('end_time', new Date(data.end_time).toISOString());
      if (data.banner_image && data.banner_image[0]) {
        formData.append('banner_image', data.banner_image[0]);
      }

      // Create draft event
      const res = await apiClient.post('/events/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      toast.success('Event draft created successfully!');

      // Navigate to the event detail page or dashboard
      navigate(`/events/${res.data.slug}`);

    } catch (error: any) {
      toast.error('Failed to create event. Please try again.');
      console.error(error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="rounded-xl border bg-card text-card-foreground shadow">
      <div className="flex justify-between border-b px-6 py-4">
        <div className={`text-sm font-medium ${step >= 1 ? 'text-forest' : 'text-muted-foreground'}`}>1. Basic Info</div>
        <div className={`text-sm font-medium ${step >= 2 ? 'text-forest' : 'text-muted-foreground'}`}>2. Timing</div>
        <div className={`text-sm font-medium ${step >= 3 ? 'text-forest' : 'text-muted-foreground'}`}>3. Media</div>
      </div>

      <div className="p-6">
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          {step === 1 && <BasicInfoStep form={form} />}
          {step === 2 && <TimingStep form={form} />}
          {step === 3 && <MediaStep form={form} />}

          <div className="flex justify-between pt-6">
            <Button
              type="button"
              variant="outline"
              onClick={prevStep}
              disabled={step === 1 || isSubmitting}
            >
              Previous
            </Button>

            {step < 3 ? (
              <Button type="button" onClick={nextStep} className="bg-forest text-white hover:bg-forest/90">
                Next Step
              </Button>
            ) : (
              <Button type="submit" disabled={isSubmitting} className="bg-amber text-forest hover:bg-amber/90 font-medium">
                {isSubmitting ? "Creating Draft..." : "Save as Draft"}
              </Button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
