import { Box, Typography } from '@mui/material';

interface ParamSelectorProps {
  params: string[];
  xValue: string;
  yValue: string;
  onXChange: (v: string) => void;
  onYChange: (v: string) => void;
}

export default function ParamSelector({ params: _params, xValue: _xValue, yValue: _yValue, onXChange: _onXChange, onYChange: _onYChange }: ParamSelectorProps) {
  return (
    <Box sx={{ p: 2, border: '1px dashed', borderColor: 'divider', borderRadius: 1 }}>
      <Typography color="text.secondary">Parameter Selector — Coming soon</Typography>
    </Box>
  );
}
