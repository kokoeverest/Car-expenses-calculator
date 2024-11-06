import * as React from 'react';
import { Typography, TypographyProps } from '@mui/material';

const StyledText: React.FC<TypographyProps> = ( { children, ...rest } ) =>
    <Typography variant="h5" sx={{color:"black"}} { ...rest }><strong>{ children }</strong></Typography>;

export default StyledText;