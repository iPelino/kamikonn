import type { UseFormReturn } from 'react-hook-form';
import type { EventFormData } from './EventWizard';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export function MediaStep({ form }: { form: UseFormReturn<EventFormData> }) {
  const { register, formState: { errors } } = form;

  return (
    <div className="space-y-6">
      <div className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="banner_image">Banner Image</Label>
          <Input
            id="banner_image"
            type="file"
            accept="image/*"
            {...register('banner_image')}
          />
          {errors.banner_image && <p className="text-sm text-red-500">{errors.banner_image.message?.toString()}</p>}
        </div>

        <div className="rounded-lg border border-dashed p-8 text-center bg-muted/30">
          <p className="text-sm text-muted-foreground">
            Upload an engaging banner image for your event. <br />
            Recommended size: 1200x630 pixels. Maximum file size: 5MB.<br />
            Supported formats: JPG, PNG, WEBP.
          </p>
        </div>
      </div>
    </div>
  );
}
