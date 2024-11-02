import React from 'react';
import { useNavigate } from 'react-router-dom';

const Header: React.FC = () =>
{

    const navigate = useNavigate();

    const handleTitleClick = () =>
    {
        navigate( '/' );
    };

    return (
        <div className="header">
            <h1 className='headerTitle' onClick={ handleTitleClick }>What's the price</h1>
        </div>
    );
};

export default Header;