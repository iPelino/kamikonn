import { useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { UploadIcon, Loader2 } from 'lucide-react';
import { apiClient } from '@/api/client';
import { toast } from 'sonner';

export function CsvImportButton() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      toast.error('Please upload a valid CSV file.');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await apiClient.post('/events/import_csv/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const { events_created, errors } = response.data;
      if (events_created > 0) {
        toast.success(`Successfully imported ${events_created} events.`);
      }

      if (errors && errors.length > 0) {
        toast.warning(`Imported with ${errors.length} errors. Check console for details.`);
        console.warn('CSV Import Errors:', errors);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to import CSV.');
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <>
      <input
        type="file"
        accept=".csv"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
      <Button
        variant="secondary"
        disabled={isUploading}
        onClick={() => fileInputRef.current?.click()}
      >
        {isUploading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <UploadIcon className="w-4 h-4 mr-2" />}
        Import CSV
      </Button>
    </>
  );
}
