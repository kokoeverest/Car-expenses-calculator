import React from 'react';
import { useNavigate } from 'react-router-dom';
import StyledText from './controls/StyledText';

const Header: React.FC = () =>
{

    const navigate = useNavigate();

    const handleTitleClick = () =>
    {
        navigate( '/' );
    };

    return (
        <div className="header">
            <StyledText 
            variant='h2' 
            className='headerTitle' 
            onClick={handleTitleClick}
            sx={{color:"yellowgreen"}}
            >
                What's the price</StyledText>
        </div>
    );
};

export default Header;