import { Box, Typography } from '@mui/material';

interface RecommendationHistoryProps {
  campaignId: string;
}

export default function RecommendationHistory({ campaignId: _campaignId }: RecommendationHistoryProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Recommendation History — Coming soon</Typography>
    </Box>
  );
}
