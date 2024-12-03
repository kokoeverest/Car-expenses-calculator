import React, { Fragment, useEffect, useRef, useState } from 'react';
import Dialog, { DialogProps } from '@mui/material/Dialog';
import { DialogTitle, DialogContent, DialogContentText, DialogActions, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, IconButton, Collapse, Box } from '@mui/material';
import StyledButton from '../../components/controls/StyledButton';
import StyledText from '../../components/controls/StyledText';
import { Car } from '../../types/car';
import { Tire } from '../../types/tire';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';

interface CarPriceResponseProps
{
    car: Car;
    open: boolean;
    onClose: () => void;
}

const CarPriceResponse: React.FC<CarPriceResponseProps> = ( {
    car: car, open, onClose } ) =>
{
    const [ scroll ] = useState<DialogProps[ 'scroll' ]>( 'paper' );
    const descriptionElementRef = useRef<HTMLElement>( null );

    const [ isCollapsed, setIsCollapsed ] = React.useState( false );
    const currencyBgn: string = " лв.";
    const fuelTypesEnToBg: { [ key: string ]: string; } = {
        "eev": "eev",
        "gasoline": "бензин",
        "diesel": "дизел",
        "lpg": "газ",
        "methane": "метан",
    };

    const fuelPerYear: ( mileage: number ) => number = ( mileage: number, car_f: Car = car ): number =>
    {
        return car_f.engine.fuel.price * car_f?.engine.consumption * mileage;

    };

    const valueToFixed: ( inputValue: number ) => string = ( inputValue: number ): string =>
    {
        return `${ inputValue.toFixed() } ${ currencyBgn }`;
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
            fullWidth={ true }
            maxWidth={ false }
        >
            <DialogTitle id="car-price-dialog-title"
                sx={ {
                    justifyItems: "center",
                    maxWidth: '100%'
                } }
            >
                <StyledText>
                    Резултат за: { car.brand.toUpperCase() } { car.model.toUpperCase() } { car.year }
                </StyledText>
            </DialogTitle>
            <DialogContent dividers={ scroll === 'paper' }>
                <DialogContentText
                    id="car-price-dialog-description"
                    ref={ descriptionElementRef }
                    tabIndex={ -1 }
                    >
                    <TableContainer component={ Paper } >
                    <Fragment>
                        <Table size="small" aria-label="a dense table" sx={ { alignItems: "center", border: 1 } }>
                            <TableHead>
                                <TableRow>
                                    <TableCell>
                                        <StyledText>
                                            Двигател: { car.engine.capacity } куб.см, { car.engine.power_hp } к.с. / { car.engine.power_kw } кВ
                                        </StyledText>
                                    </TableCell>
                                    <TableCell colSpan={ 2 }>
                                        <StyledText>
                                            Ср. разход: <StyledText sx={ { color: 'orange', display: 'inline' } }>{ car.engine?.consumption.toFixed( 1 ) } л/100км</StyledText>
                                        </StyledText>
                                    </TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell><StyledText>Застраховка ГО за една година: </StyledText></TableCell>
                                    <TableCell><StyledText variant="h6">Най-ниска цена</StyledText></TableCell>
                                    <TableCell><StyledText variant="h6">Най-висока цена</StyledText></TableCell>
                                </TableRow>

                                <TableRow sx={ { '&:last-child td, &:last-child th': { border: 0 } } }>
                                    <TableCell colSpan={ 1 }></TableCell>
                                    <TableCell>
                                        <StyledText sx={ { color: 'green' } }>{ valueToFixed( car.insurance.min_price ) }</StyledText>
                                    </TableCell>
                                    <TableCell>
                                        <StyledText sx={ { color: 'red' } }>{ valueToFixed( car.insurance.max_price ) }</StyledText>
                                    </TableCell>
                                </TableRow>
                                <TableRow>

                                    <TableCell>
                                        <StyledText>Годишен данък (град { car.tax.municipality }): </StyledText>

                                    </TableCell>
                                    <TableCell colSpan={ 2 }><StyledText sx={ { color: 'green' } }>{ valueToFixed( car.tax.price ) }</StyledText></TableCell>
                                </TableRow>
                                <TableRow>
                                    <TableCell>
                                        <StyledText>Цена за гориво за 1 година при годишен пробег:</StyledText>
                                    </TableCell>
                                    <TableCell >
                                        <StyledText sx={ { color: 'green' } }> 10000 км</StyledText>
                                    </TableCell>

                                    <TableCell>
                                        <StyledText sx={ { color: 'red' } }>20000 км</StyledText>
                                    </TableCell>
                                </TableRow>
                                <TableCell colSpan={ 1 }>
                                    <StyledText>(актуална цена { car.engine.fuel.price.toFixed( 2 ) } { currencyBgn }/л { fuelTypesEnToBg[ car.engine.fuel.fuel_type ] })</StyledText>
                                </TableCell>
                                <TableCell>
                                    <StyledText sx={ { color: 'green' } }> { valueToFixed( fuelPerYear( 100 ) ) }</StyledText>
                                </TableCell>
                                <TableCell>
                                    <StyledText sx={ { color: 'red' } }>{ valueToFixed( fuelPerYear( 200 ) ) }</StyledText>
                                </TableCell>
                            </TableHead>
                                <TableRow sx={ { '& > *': { borderBottom: 'unset' } } }>
                                    <TableCell>
                                        <StyledText variant="h6" sx={ { color: 'black', display: "inline" } }>Размер гуми:</StyledText></TableCell>
                                        <IconButton
                                            aria-label="expand row"
                                            size="medium"
                                            onClick={ () => setIsCollapsed( !isCollapsed ) }
                                        >
                                            { isCollapsed ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon /> }
                                        </IconButton>
                                    <TableCell><StyledText variant="h6">Най-ниска цена</StyledText></TableCell>
                                    <TableCell><StyledText variant="h6">Най-висока цена</StyledText></TableCell>
                                </TableRow>

                                { car.tires.map( ( tire: Tire ) => (
                                    <TableRow
                                        key={ tire.size }
                                    >
                                        <TableCell style={ { paddingBottom: 0, paddingTop: 0 } } colSpan={ 3 }>
                                            <Collapse in={ isCollapsed } timeout="auto" unmountOnExit>
                                                <Box>
                                                    <Table>
                                                        <TableHead>
                                                            <TableRow>
                                                                <TableCell component="th" scope="row" align="left">
                                                                    <StyledText variant="h6">{ tire.width }/{ tire.height }/{ tire.prefix }/{ tire.size }</StyledText>
                                                                </TableCell>
                                                                <TableCell>
                                                                    <StyledText variant='h6' sx={ { color: 'green' } }>{ valueToFixed( tire.min_price ) }</StyledText>
                                                                </TableCell>
                                                                <TableCell>
                                                                    <StyledText variant='h6' sx={ { color: 'red' } }>{ valueToFixed( tire.max_price ) }</StyledText>
                                                                </TableCell>
                                                            </TableRow>
                                                        </TableHead>
                                                    </Table>
                                                </Box>
                                            </Collapse>
                                        </TableCell>
                                    </TableRow>
                                ) ) }
                        </Table>
                            </Fragment>
                    </TableContainer>
                </DialogContentText>
            </DialogContent>
            <DialogActions sx={ { placeContent: "center" } }>
                <div>
                    <StyledButton onClick={ onClose }>Затвори</StyledButton>
                </div>
            </DialogActions>
        </Dialog >

    );
};

export default CarPriceResponse;