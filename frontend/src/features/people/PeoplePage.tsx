import { useState } from 'react';
import { type GridColDef } from '@mui/x-data-grid';
import { Button, Chip } from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import PageHeader from '@/components/PageHeader';
import DataTable from '@/components/DataTable';
import ConfirmDialog from '@/components/ConfirmDialog';
import { usePaginationParams } from '@/utils/pagination';
import { usePeople, useDeletePerson, type Person } from './hooks';
import PersonFormDialog from './PersonFormDialog';
import { useNotification } from '@/components/NotificationProvider';

export default function PeoplePage() {
  const { params, paginationModel, sortModel, onPaginationModelChange, onSortModelChange, setSearch, setIncludeRetired } =
    usePaginationParams('name');
  const { data, isLoading } = usePeople(params);
  const deletePerson = useDeletePerson();
  const { notify } = useNotification();

  const [formOpen, setFormOpen] = useState(false);
  const [editPerson, setEditPerson] = useState<Person | null>(null);
  const [retireTarget, setRetireTarget] = useState<Person | null>(null);

  const handleRetire = async () => {
    if (retireTarget) {
      await deletePerson.mutateAsync(retireTarget.id);
      notify('Person retired');
      setRetireTarget(null);
      setFormOpen(false);
    }
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', flex: 1, minWidth: 150 },
    {
      field: 'is_default', headerName: 'Default', width: 100,
      renderCell: (params) => params.value ? <Chip label="Default" size="small" color="primary" /> : null,
    },
  ];

  return (
    <>
      <PageHeader title="People"
        actions={<Button variant="contained" startIcon={<AddIcon />} onClick={() => { setEditPerson(null); setFormOpen(true); }}>Add Person</Button>}
      />
      <DataTable<Person>
        columns={columns} rows={data?.items ?? []} total={data?.total ?? 0} loading={isLoading}
        paginationModel={paginationModel} onPaginationModelChange={onPaginationModelChange}
        sortModel={sortModel} onSortModelChange={onSortModelChange}
        search={params.q} onSearchChange={setSearch}
        includeRetired={params.include_retired} onIncludeRetiredChange={setIncludeRetired}
        onRowClick={(row) => { setEditPerson(row); setFormOpen(true); }}
        emptyTitle="No people yet" emptyActionLabel="Add Person"
        onEmptyAction={() => { setEditPerson(null); setFormOpen(true); }}
      />
      <PersonFormDialog
        open={formOpen}
        onClose={() => setFormOpen(false)}
        person={editPerson}
        onRetire={editPerson ? () => setRetireTarget(editPerson) : undefined}
      />
      <ConfirmDialog open={!!retireTarget} title="Retire Person"
        message={`Retire "${retireTarget?.name}"? This won't delete their brews or ratings.`}
        onConfirm={handleRetire} onCancel={() => setRetireTarget(null)} />
    </>
  );
}
