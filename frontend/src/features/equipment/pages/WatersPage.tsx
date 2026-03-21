import { useState } from 'react';
import { type GridColDef } from '@mui/x-data-grid';
import { Button, IconButton, Stack } from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Archive as ArchiveIcon } from '@mui/icons-material';
import PageHeader from '@/components/PageHeader';
import DataTable from '@/components/DataTable';
import ConfirmDialog from '@/components/ConfirmDialog';
import { usePaginationParams } from '@/utils/pagination';
import { waterHooks, type Water } from '../hooks';
import WaterFormDialog from '../components/WaterFormDialog';
import { useNotification } from '@/components/NotificationProvider';

export default function WatersPage() {
  const { params, paginationModel, sortModel, onPaginationModelChange, onSortModelChange, setSearch, setIncludeRetired } =
    usePaginationParams('name');
  const { data, isLoading } = waterHooks.useList(params);
  const deleteWater = waterHooks.useDelete();
  const { notify } = useNotification();

  const [formOpen, setFormOpen] = useState(false);
  const [editWater, setEditWater] = useState<Water | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Water | null>(null);

  const handleDelete = async () => {
    if (deleteTarget) {
      await deleteWater.mutateAsync(deleteTarget.id);
      notify('Water retired');
      setDeleteTarget(null);
    }
  };

  const columns: GridColDef[] = [
    { field: 'name', headerName: 'Name', flex: 1, minWidth: 150 },
    {
      field: 'minerals',
      headerName: 'Minerals',
      flex: 1,
      minWidth: 100,
      renderCell: (params) => params.row.minerals.length,
    },
    {
      field: 'actions',
      headerName: '',
      width: 88,
      sortable: false,
      renderCell: (params) => (
        <Stack direction="row" spacing={0.5} alignItems="center" height="100%">
          <IconButton
            size="small"
            aria-label="Edit water"
            onClick={(e) => {
              e.stopPropagation();
              setEditWater(params.row as Water);
              setFormOpen(true);
            }}
          >
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            aria-label="Retire water"
            onClick={(e) => {
              e.stopPropagation();
              setDeleteTarget(params.row as Water);
            }}
          >
            <ArchiveIcon fontSize="small" />
          </IconButton>
        </Stack>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Waters"
        actions={
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => { setEditWater(null); setFormOpen(true); }}
          >
            Add Water
          </Button>
        }
      />
      <DataTable<Water>
        columns={columns}
        rows={data?.items ?? []}
        total={data?.total ?? 0}
        loading={isLoading}
        paginationModel={paginationModel}
        onPaginationModelChange={onPaginationModelChange}
        sortModel={sortModel}
        onSortModelChange={onSortModelChange}
        search={params.q}
        onSearchChange={setSearch}
        includeRetired={params.include_retired}
        onIncludeRetiredChange={setIncludeRetired}
        emptyTitle="No waters yet"
        emptyActionLabel="Add Water"
        onEmptyAction={() => { setEditWater(null); setFormOpen(true); }}
      />
      <WaterFormDialog open={formOpen} onClose={() => setFormOpen(false)} water={editWater} />
      <ConfirmDialog
        open={!!deleteTarget}
        title="Retire Water"
        message={`Retire "${deleteTarget?.name}"?`}
        onConfirm={handleDelete}
        onCancel={() => setDeleteTarget(null)}
      />
    </>
  );
}
