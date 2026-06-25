import type { UseFormReturn } from 'react-hook-form';
import type { EventFormData } from './EventWizard';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { useQuery } from '@tanstack/react-query';
import apiClient from '@/api/client';

export function BasicInfoStep({ form }: { form: UseFormReturn<EventFormData> }) {
  const { register, watch, setValue, formState: { errors } } = form;
  const isVirtual = watch('is_virtual');

  const { data: categories = [] } = useQuery({
    queryKey: ['categories'],
    queryFn: async () => {
      const res = await apiClient.get('/categories/');
      return res.data;
    }
  });

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label htmlFor="title">Event Title <span className="text-red-500">*</span></Label>
        <Input
          id="title"
          placeholder="e.g. AI in Healthcare Symposium"
          {...register('title')}
        />
        {errors.title && <p className="text-sm text-red-500">{errors.title.message}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          placeholder="Describe your event..."
          className="h-32"
          {...register('description')}
        />
        {errors.description && <p className="text-sm text-red-500">{errors.description.message}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="category">Category</Label>
        <select
          id="category"
          className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
          {...register('category')}
        >
          <option value="">Select a category</option>
          {categories.map((cat: any) => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      <div className="flex items-center space-x-2 rounded-lg border p-4">
        <Switch
          id="is_virtual"
          checked={isVirtual}
          onCheckedChange={(checked) => setValue('is_virtual', checked, { shouldValidate: true })}
        />
        <div className="space-y-0.5">
          <Label htmlFor="is_virtual" className="text-base">Virtual Event</Label>
          <p className="text-sm text-muted-foreground">Is this an online-only event?</p>
        </div>
      </div>

      {!isVirtual && (
        <div className="space-y-2">
          <Label htmlFor="location">Physical Location</Label>
          <Input
            id="location"
            placeholder="e.g. ALU Campus, Innovation Hub"
            {...register('location')}
          />
        </div>
      )}
    </div>
  );
}
