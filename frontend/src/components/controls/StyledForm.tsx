import * as React from 'react';
import Box, { BoxProps } from '@mui/material/Box';


const StyledForm: React.FC<BoxProps> = ( { children, ...rest } ) => (
    <Box
        component="form"
        sx={ {
            m: 'auto',
            p: 2,
            borderRadius: '10px',
            position: 'sticky',
            alignItems: 'center',
            justifyContent: 'center',
            border: '1px solid var(--backGroundOrange)',
            gridTemplateColumns: 'repeat(auto-fit, minmax(600px, 1fr))',
            '& .MuiTextField-root': { m: 2, width: '80%' },
            maxWidth: '80%',
            backgroundColor: 'lightgrey',//'var(--formGrey)',
            color: 'black'
        } }
        { ...rest }
    >
        { children }
    </Box>
);

export default StyledForm; 