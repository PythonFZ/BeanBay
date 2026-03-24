import { Box, Typography } from '@mui/material';

interface FeatureImportanceProps {
  campaignId: string;
}

export default function FeatureImportance({ campaignId: _campaignId }: FeatureImportanceProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Feature Importance — Coming soon</Typography>
    </Box>
  );
}
