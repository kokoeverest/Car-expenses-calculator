import React from "react";
import { Button, ButtonProps } from "@mui/material";
import './Button.css';
import StyledText from "./StyledText";

const StyledButton: React.FC<ButtonProps> = ( { children, ...rest } ) => (
    <Button variant="contained" sx={ { color: 'black', width: 'auto', m: 1, p: 1 } } { ...rest } >
        <StyledText variant="body2">
            { children }
        </StyledText>

    </Button>
);

export default StyledButton;