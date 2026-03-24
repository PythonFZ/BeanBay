import { Box, Typography } from '@mui/material';

interface PredictionSurfaceProps {
  campaignId: string;
  params: string[];
  defaultX: string;
  defaultY: string;
}

export default function PredictionSurface({ campaignId: _campaignId, params: _params, defaultX: _defaultX, defaultY: _defaultY }: PredictionSurfaceProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Prediction Surface — Coming soon</Typography>
    </Box>
  );
}
