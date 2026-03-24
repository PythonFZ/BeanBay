import { Box, Typography } from '@mui/material';

interface UncertaintySurfaceProps {
  campaignId: string;
  params: string[];
  defaultX: string;
  defaultY: string;
}

export default function UncertaintySurface({ campaignId: _campaignId, params: _params, defaultX: _defaultX, defaultY: _defaultY }: UncertaintySurfaceProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Uncertainty Surface — Coming soon</Typography>
    </Box>
  );
}
