import { Box, Typography } from '@mui/material';

interface ParameterHeatmapProps {
  campaignId: string;
  params: string[];
  defaultX: string;
  defaultY: string;
}

export default function ParameterHeatmap({ campaignId: _campaignId, params: _params, defaultX: _defaultX, defaultY: _defaultY }: ParameterHeatmapProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Parameter Heatmap — Coming soon</Typography>
    </Box>
  );
}
