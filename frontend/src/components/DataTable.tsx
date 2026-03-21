// frontend/src/components/DataTable.tsx
import { useCallback, useState } from 'react';
import {
  DataGrid, type GridColDef, type GridPaginationModel,
  type GridRowParams, type GridSortModel,
} from '@mui/x-data-grid';
import { Box, FormControlLabel, Switch, TextField, InputAdornment } from '@mui/material';
import { Search as SearchIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router';
import EmptyState from '@/components/EmptyState';

interface DataTableProps<T extends { id: string }> {
  columns: GridColDef[];
  rows: T[];
  total: number;
  loading: boolean;
  paginationModel: GridPaginationModel;
  onPaginationModelChange: (model: GridPaginationModel) => void;
  sortModel: GridSortModel;
  onSortModelChange: (model: GridSortModel) => void;
  search?: string;
  onSearchChange?: (q: string) => void;
  includeRetired?: boolean;
  onIncludeRetiredChange?: (include: boolean) => void;
  detailPath?: (row: T) => string;
  emptyTitle?: string;
  emptyDescription?: string;
  emptyActionLabel?: string;
  onEmptyAction?: () => void;
}

export default function DataTable<T extends { id: string }>({
  columns, rows, total, loading, paginationModel, onPaginationModelChange,
  sortModel, onSortModelChange, search, onSearchChange, includeRetired,
  onIncludeRetiredChange, detailPath, emptyTitle = 'No items yet',
  emptyDescription, emptyActionLabel, onEmptyAction,
}: DataTableProps<T>) {
  const navigate = useNavigate();
  const [searchInput, setSearchInput] = useState(search ?? '');

  const handleSearchSubmit = useCallback(() => {
    onSearchChange?.(searchInput);
  }, [onSearchChange, searchInput]);

  const handleRowClick = useCallback(
    (params: GridRowParams<T>) => {
      if (detailPath) navigate(detailPath(params.row));
    },
    [navigate, detailPath],
  );

  if (!loading && rows.length === 0 && !search && !includeRetired) {
    return (
      <EmptyState title={emptyTitle} description={emptyDescription}
        actionLabel={emptyActionLabel} onAction={onEmptyAction} />
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap', alignItems: 'center' }}>
        {onSearchChange && (
          <TextField size="small" placeholder="Search..." value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSearchSubmit()}
            onBlur={handleSearchSubmit}
            slotProps={{
              input: {
                startAdornment: (
                  <InputAdornment position="start"><SearchIcon fontSize="small" /></InputAdornment>
                ),
              },
            }}
            sx={{ maxWidth: 300 }}
          />
        )}
        {onIncludeRetiredChange && (
          <FormControlLabel
            control={<Switch size="small" checked={includeRetired ?? false}
              onChange={(_, checked) => onIncludeRetiredChange(checked)} />}
            label="Show retired"
          />
        )}
      </Box>
      <DataGrid
        rows={rows} columns={columns} rowCount={total} loading={loading}
        paginationMode="server" paginationModel={paginationModel}
        onPaginationModelChange={onPaginationModelChange} pageSizeOptions={[10, 25, 50]}
        sortingMode="server" sortModel={sortModel} onSortModelChange={onSortModelChange}
        onRowClick={handleRowClick} disableRowSelectionOnClick autoHeight
        sx={{
          border: 0, cursor: detailPath ? 'pointer' : 'default',
          '& .MuiDataGrid-row:hover': detailPath ? { bgcolor: 'action.hover' } : {},
        }}
      />
    </Box>
  );
}
