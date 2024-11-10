import React, { useEffect, useRef, useState } from 'react';
import Dialog, { DialogProps } from '@mui/material/Dialog';
import { DialogContent, DialogContentText, DialogActions } from '@mui/material';
import StyledButton from '../../components/controls/StyledButton';
import StyledText from '../../components/controls/StyledText';

interface CarPriceNotFoundResponseProps
{
    brand: string;
    model: string;
    year: string;
    open: boolean;
    onClose: () => void;
}

const CarPriceNotFoundResponse: React.FC<CarPriceNotFoundResponseProps> = ( {
    brand: brand, model: model, year: year, open, onClose } ) =>
{
    const [ scroll ] = useState<DialogProps[ 'scroll' ]>( 'paper' );
    const descriptionElementRef = useRef<HTMLElement>( null );

    useEffect( (): void =>
    {
        if ( open && descriptionElementRef.current )
        {
            descriptionElementRef.current.focus();
        }
    }, [ open ] );

    return (
        <Dialog
            open={ open }
            onClose={ onClose }
            scroll={ scroll }
            aria-labelledby="car-price-dialog-errorResponse"
            aria-describedby="car-price-dialog-errorResponse-description"
            maxWidth={ "md" }
        >
            <DialogContent dividers={ scroll === 'paper' }>
                <DialogContentText
                    id="car-price-dialog-errorResponse-description"
                    ref={ descriptionElementRef }
                    tabIndex={ -1 }
                    sx={ {
                        justifyItems: "center",
                        maxWidth: '100%'
                    } }
                >
                    <StyledText>
                        Резултат за: { brand.toUpperCase() } { model.toUpperCase() } { year } не е открит :(
                    </StyledText>

                </DialogContentText>
            </DialogContent>
            <DialogActions sx={ { placeContent: "center" } }>
                <div>
                    <StyledButton onClick={ onClose }>Затвори</StyledButton>
                </div>
            </DialogActions>
        </Dialog>

    );
};

export default CarPriceNotFoundResponse;