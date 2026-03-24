import { Box, Typography } from '@mui/material';
import type { ScoreHistoryEntry } from '../hooks';

interface ScoreProgressChartProps {
  history: ScoreHistoryEntry[];
}

export default function ScoreProgressChart({ history: _history }: ScoreProgressChartProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Score Progress Chart — Coming soon</Typography>
    </Box>
  );
}
