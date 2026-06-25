import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { fetchUniversities, createUniversity, updateUniversity, assignModerator, removeModerator } from '../api/universitiesApi';
import type { University } from '../api/universitiesApi';
import { toast } from 'sonner';
import { Loader2, Plus, Edit2, Users, ShieldAlert, X } from 'lucide-react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Switch } from '@/components/ui/switch';

export function UniversityManagementPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [isModOpen, setIsModOpen] = useState(false);
  const [selectedUniv, setSelectedUniv] = useState<University | null>(null);

  const queryClient = useQueryClient();

  const { data: universities = [], isLoading } = useQuery({
    queryKey: ['universities'],
    queryFn: fetchUniversities,
  });

  const filtered = universities.filter(u =>
    u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    u.short_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEdit = (u: University) => {
    setSelectedUniv(u);
    setIsFormOpen(true);
  };

  const handleMods = (u: University) => {
    setSelectedUniv(u);
    setIsModOpen(true);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Universities</h1>
          <p className="text-muted-foreground">Manage universities and moderators</p>
        </div>
        <Button onClick={() => { setSelectedUniv(null); setIsFormOpen(true); }}>
          <Plus className="w-4 h-4 mr-2" />
          Add University
        </Button>
      </div>

      <div className="mb-6">
        <Input
          placeholder="Search universities..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="max-w-md"
        />
      </div>

      {isLoading ? (
        <div className="flex justify-center py-12"><Loader2 className="w-8 h-8 animate-spin" /></div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filtered.map(univ => (
            <Card key={univ.id} className={!univ.is_active ? 'opacity-60' : ''}>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-lg font-bold">{univ.short_name}</CardTitle>
                <div className="flex gap-2">
                  <Button variant="ghost" size="icon" onClick={() => handleEdit(univ)}>
                    <Edit2 className="w-4 h-4 text-muted-foreground" />
                  </Button>
                  <Button variant="ghost" size="icon" onClick={() => handleMods(univ)}>
                    <Users className="w-4 h-4 text-muted-foreground" />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <p className="font-medium">{univ.name}</p>
                <p className="text-sm text-muted-foreground mb-4">{univ.domain}</p>

                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <ShieldAlert className="w-4 h-4" />
                  {univ.moderators?.length || 0} Moderators
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Forms and Modals would go here, simplified for brevity */}
      {isFormOpen && (
        <UniversityFormDialog
          univ={selectedUniv}
          open={isFormOpen}
          onOpenChange={setIsFormOpen}
          onSuccess={() => queryClient.invalidateQueries({ queryKey: ['universities'] })}
        />
      )}

      {isModOpen && selectedUniv && (
        <ModeratorDialog
          univ={selectedUniv}
          open={isModOpen}
          onOpenChange={setIsModOpen}
          onSuccess={() => queryClient.invalidateQueries({ queryKey: ['universities'] })}
        />
      )}
    </div>
  );
}

function UniversityFormDialog({ univ, open, onOpenChange, onSuccess }: any) {
  const [formData, setFormData] = useState({
    name: univ?.name || '',
    short_name: univ?.short_name || '',
    domain: univ?.domain || '',
    logo_url: univ?.logo_url || '',
    is_active: univ !== undefined ? univ.is_active : true,
  });

  const mutation = useMutation({
    mutationFn: (data: Partial<University>) => univ ? updateUniversity(univ.id, data) : createUniversity(data),
    onSuccess: () => {
      toast.success(univ ? 'Updated successfully' : 'Created successfully');
      onSuccess();
      onOpenChange(false);
    },
    onError: () => toast.error('Failed to save university')
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{univ ? 'Edit University' : 'Add University'}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 mt-4">
          <div>
            <label className="text-sm font-medium">Name</label>
            <Input value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required />
          </div>
          <div>
            <label className="text-sm font-medium">Short Name</label>
            <Input value={formData.short_name} onChange={e => setFormData({...formData, short_name: e.target.value})} required />
          </div>
          <div>
            <label className="text-sm font-medium">Domain</label>
            <Input value={formData.domain} onChange={e => setFormData({...formData, domain: e.target.value})} required />
          </div>
          <div>
            <label className="text-sm font-medium">Logo URL</label>
            <Input value={formData.logo_url} onChange={e => setFormData({...formData, logo_url: e.target.value})} />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium">Active Status</label>
            <Switch checked={formData.is_active} onCheckedChange={(c: boolean) => setFormData({...formData, is_active: c})} />
          </div>
          <div className="flex justify-end pt-4">
            <Button type="submit" disabled={mutation.isPending}>Save</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}

function ModeratorDialog({ univ, open, onOpenChange, onSuccess }: any) {
  const [userId, setUserId] = useState('');

  const assignMut = useMutation({
    mutationFn: () => assignModerator(univ.id, parseInt(userId)),
    onSuccess: () => {
      toast.success('Moderator assigned');
      setUserId('');
      onSuccess();
    },
    onError: () => toast.error('Failed to assign')
  });

  const removeMut = useMutation({
    mutationFn: (id: number) => removeModerator(univ.id, id),
    onSuccess: () => {
      toast.success('Moderator removed');
      onSuccess();
    },
    onError: () => toast.error('Failed to remove')
  });

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Manage Moderators: {univ.short_name}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 mt-4">
          <div className="flex gap-2">
            <Input placeholder="User ID" value={userId} onChange={e => setUserId(e.target.value)} type="number" />
            <Button onClick={() => assignMut.mutate()} disabled={!userId || assignMut.isPending}>Add</Button>
          </div>

          <div className="mt-6 border rounded-md divide-y">
            {univ.moderators?.length === 0 ? (
              <div className="p-4 text-center text-sm text-muted-foreground">No moderators assigned</div>
            ) : (
              univ.moderators.map((m: any) => (
                <div key={m.id} className="flex justify-between items-center p-3">
                  <div>
                    <p className="text-sm font-medium">{m.first_name} {m.last_name}</p>
                    <p className="text-xs text-muted-foreground">{m.email}</p>
                  </div>
                  <Button variant="ghost" size="icon" onClick={() => removeMut.mutate(m.id)}>
                    <X className="w-4 h-4 text-destructive" />
                  </Button>
                </div>
              ))
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
