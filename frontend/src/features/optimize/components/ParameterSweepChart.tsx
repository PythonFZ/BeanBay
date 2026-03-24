import { Box, Typography } from '@mui/material';

interface ParameterSweepChartProps {
  campaignId: string;
  param: string;
}

export default function ParameterSweepChart({ campaignId: _campaignId, param: _param }: ParameterSweepChartProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Parameter Sweep Chart — Coming soon</Typography>
    </Box>
  );
}
