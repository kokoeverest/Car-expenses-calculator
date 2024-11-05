import React, { useEffect, useRef, useState } from 'react';
import Dialog, { DialogProps } from '@mui/material/Dialog';
import { DialogTitle, DialogContent, DialogContentText, DialogActions } from '@mui/material';
import StyledButton from '../components/controls/StyledButton';
import StyledText from '../components/controls/StyledText';
import { Car } from '../types/car';

interface CarPriceResultProps
{
    car: Car | null;
    open: boolean;
    onClose: () => void;
}

const CarPriceResult: React.FC<CarPriceResultProps> = ( {
    car: car, open, onClose } ) =>
{
    const [ scroll ] = useState<DialogProps[ 'scroll' ]>( 'paper' );
    const descriptionElementRef = useRef<HTMLElement>( null );
    const currencyBgn: string = "лв";

    const fuelPerYear: ( mileage: number ) => number = ( mileage: number, car_f: Car | null = car ): number =>
    {
        return car_f?.engine?.fuel.price! * car_f?.engine.consumption! * mileage;

    };

    const valueToFixed: ( inputString: number ) => string = ( inputString: number ): string =>
    {
        return inputString.toFixed( 2 );
    };

    useEffect( (): void =>
    {
        if ( open && descriptionElementRef.current )
        {
            descriptionElementRef.current.focus();
        }
    }, [ open ] );

    if ( !car ) return null;

    return (
        <Dialog
            open={ open }
            onClose={ onClose }
            scroll={ scroll }
            aria-labelledby="car-price-dialog--title"
            aria-describedby="car-price-dialog-description"
            sx={ { lineHeight: 2 } }
        >
            <DialogTitle id="car-price-dialog-title"
                sx={ {
                    width: '90%',
                    maxWidth: '100%'
                } }
            >
                <StyledText>
                    Резултат за: { car.brand } { car.model } { car.year }
                </StyledText>
            </DialogTitle>
            <DialogContent dividers={ scroll === 'paper' }>
                <DialogContentText
                    id="car-price-dialog-description"
                    ref={ descriptionElementRef }
                    tabIndex={ -1 }
                >
                    <StyledText>Двигател: { car.engine?.capacity } куб.см, { car.engine?.power_hp } к.с</StyledText>
                    <StyledText>Ср.разход: { valueToFixed( car.engine?.consumption ) } л/100км</StyledText>
                    <StyledText>Цена за гориво за 1 година при</StyledText>
                    <StyledText>
                        <StyledText variant='h4' sx={ { color: 'green', display: 'inline' } }> 10000 / </StyledText>
                        <StyledText variant='h4' sx={ { color: 'orange', display: 'inline' } }>20000 / </StyledText>
                        <StyledText variant='h4' sx={ { color: 'red', display: 'inline' } }>30000</StyledText> км пробег:
                    </StyledText>
                    <StyledText>
                        <StyledText variant='h4' sx={ { color: 'green', display: 'inline' } }> { fuelPerYear( 100 ).toFixed() } / </StyledText>
                        <StyledText variant='h4' sx={ { color: 'orange', display: 'inline' } }>{ fuelPerYear( 200 ).toFixed() } / </StyledText>
                        <StyledText variant='h4' sx={ { color: 'red', display: 'inline' } }>{ fuelPerYear( 300 ).toFixed() } { currencyBgn }</StyledText>
                    </StyledText>
                    <StyledText>Застраховка Гражданска отговорност за една година: </StyledText>
                    <StyledText variant='h4' sx={ { color: 'green', display: 'inline' } }> от { valueToFixed( car.insurance?.min_price ) } { currencyBgn }</StyledText>
                    <StyledText variant='h4' sx={ { color: 'red', display: 'inline' } }> до { valueToFixed( car.insurance?.max_price ) } { currencyBgn }</StyledText>
                    <StyledText></StyledText>
                    <StyledText></StyledText>

                </DialogContentText>
            </DialogContent>
            <DialogActions>
                <div>
                    <StyledButton onClick={ onClose }>Close</StyledButton>
                </div>
            </DialogActions>
        </Dialog>

    );
};

export default CarPriceResult;