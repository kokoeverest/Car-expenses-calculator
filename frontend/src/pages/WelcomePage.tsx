import React from 'react';
import { useNavigate } from 'react-router-dom';
import StyledButton from '../components/controls/StyledButton';
import { Box, Divider } from '@mui/material';
import StyledText from '../components/controls/StyledText';

const WelcomePage: React.FC = () =>
{
    const navigate = useNavigate();
    const handleExploreClick = () =>
    {
        navigate( '/form' );
    };

    return (
        <>
            <Box sx={ { p: 5 } }>
                <StyledText variant='h2'>Welcome to 'Is it expensive?'</StyledText>
                <StyledText variant='h4'>The place where you know how much a car costs</StyledText>
            </Box>
            <Box className="welcome-page">
                <Divider></Divider>
                    <StyledButton onClick={ handleExploreClick }>Click to search for a car</StyledButton>
            </Box>
        </>
    );
};

export default WelcomePage;