import React, { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { Checkbox, CircularProgress, FormControlLabel, InputAdornment, MenuItem, TextField } from "@mui/material";
import { useMutation, UseMutationResult, useQuery, useQueryClient, UseQueryResult } from "@tanstack/react-query";
import StyledButton from "../components/controls/StyledButton";
import StyledFormDesktop from "../components/controls/StyledFormDesktop";
import { CarDetailFormInput } from "./abstract";
import carApi from "../api/carApi";
import CarDetailsSchema from "./schemas";
import CarPriceResponse from "./responses/CarPriceResponse";
import { Car } from "../types/car";
import StyledText from "../components/controls/StyledText";
import CarPriceNotFoundResponse from "./responses/CarPriceNotFoundResponse";

const CarDetailsForm: React.FC = () =>
{
    const queryClient = useQueryClient();

    const [ selectedCarBrand, setSelectedCarBrand ] = useState( '' );
    const [ selectedModel, setSelectedModel ] = useState( '' );
    const [ selectedCity, setSelectedCity ] = useState( 'София' );
    const [ selectedFuelType, setSelectedFuelType ] = useState( 'diesel' );
    const [ selectedYear, setSelectedYear ] = useState( '' );
    const [ openDialog, setOpenDialog ] = useState( false );
    const [ carData, setCarData ] = useState<Car | null>( null );
    const [ isKw, setIsKw ] = useState( false );

    const handleToggle = () =>
    {
        setIsKw( ( prev ) => !prev );
        setValue( isKw ? "power_hp" : "power_kw", "" );
    };


    const fuelTypesBgToEn: { [ key: string ]: string; } = {
        "eev": "eev",
        "бензин": "gasoline",
        "дизел": "diesel",
        "газ": "lpg",
        "метан": "methane",
    };

    const {
        register,
        handleSubmit,
        setValue,
        formState: { errors },
    } = useForm<CarDetailFormInput>( {
        resolver: yupResolver( CarDetailsSchema ),
    } );

    const brandsQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ "getCarBrands" ],
        queryFn: carApi.getCarBrands
    } );

    const carModelsQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ "getCarModels", selectedCarBrand ],
        queryFn: (): Promise<string[]> => carApi.getModels( selectedCarBrand! ),
        enabled: selectedCarBrand !== "",
    } );

    const modelYearsQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ "getModelYears", selectedCarBrand, selectedModel ],
        queryFn: (): Promise<string[]> => carApi.getModelYears( selectedCarBrand!, selectedModel! ),
        enabled: selectedModel !== "",
    } );

    const citiesQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ 'getCities' ],
        queryFn: carApi.getCities,
    } );

    const mutation: UseMutationResult<Car, Error, CarDetailFormInput, unknown> = useMutation( {
        mutationFn: carApi.getCarPrice,
        onSuccess: ( data: Car ): void =>
        {
            setCarData( data );
            setOpenDialog( true );
            queryClient.invalidateQueries( { queryKey: [ 'getCarBrands', 'getCarModels', 'getCities' ] } );
        },
        onError: (): void =>
        {
            setOpenDialog( true );
        }
    } );

    const onSubmitHandler: SubmitHandler<CarDetailFormInput> = async ( data: CarDetailFormInput ): Promise<void> =>
    {
        mutation.mutate( data );
        console.log( "the formInput data", data );
    };

    useEffect( (): void =>
    {
        setSelectedModel( '' );
    }, [ selectedCarBrand ] );

    useEffect( (): void =>
    {
        setSelectedYear( '' );
    }, [ selectedModel ] );

    return (
        <>
            { !mutation.isPending && (
                <StyledFormDesktop onSubmit={ handleSubmit( onSubmitHandler ) }>
                    <StyledText variant="h4">Въведете данни за автомобила</StyledText>

                    <TextField
                        { ...register( "brand" ) }
                        select
                        label="Марка"
                        error={ !!errors.brand }
                        helperText={ "Изберете марка автомобил" }
                        value={ selectedCarBrand }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedCarBrand( event.target.value ) }
                    >
                        { brandsQuery.data?.map( ( brand: string ) => (
                            <MenuItem key={ brand } value={ brand }>
                                { brand }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'model' ) }
                        select
                        label="Модел"
                        error={ !!errors.model }
                        helperText={ "Изберете модел" }
                        value={ selectedModel }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedModel( event.target.value ) }
                    >
                        { carModelsQuery.data?.map( ( model: string ) => (
                            <MenuItem key={ model } value={ model }>
                                { model }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'year' ) }
                        select
                        label="Година"
                        error={ !!errors.year }
                        value={ selectedYear }
                        helperText={ "Изберете година на производство" }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedYear( event.target.value ) }
                    >
                        { modelYearsQuery.data?.map( ( year: string ) => (
                            <MenuItem key={ year } value={ year }>
                                { year }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'fuel_type' ) }
                        label="Вид гориво"
                        select
                        error={ !!errors.fuel_type }
                        helperText={ "Изберете гориво" }
                        value={ selectedFuelType }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedFuelType( event.target.value ) }
                    >
                        { Object.entries( fuelTypesBgToEn ).map( ( key: [ string, string ], value ) => (
                            <MenuItem key={ value } value={ key[ 1 ] }>
                                { key[ 0 ] }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'engine_capacity' ) }
                        label="Обем на двигателя"
                        type="text"
                        error={ !!errors.engine_capacity }
                        helperText={ "Обем на двигателя" }
                    />

                    <TextField
                        { ...register( isKw ? "power_kw" : "power_hp" ) }
                        label={ `Мощност в ${ isKw ? "кВ" : "к.с." }` }
                        type="text"
                        placeholder={ `Мощност в ${ isKw ? "кВ" : "к.с." }` }
                        error={ isKw ? !!errors.power_kw : !!errors.power_hp }
                        helperText={ isKw ? "Мощност в кВ" : "Мощност в к.с." }
                        slotProps={ {
                            input: {
                                endAdornment: (
                                    <InputAdornment position="end">
                                        <FormControlLabel
                                            control={
                                                <Checkbox
                                                    checked={ isKw }
                                                    onChange={ handleToggle }
                                                />
                                            }
                                            label="кВ"
                                        />
                                    </InputAdornment>
                                ),
                            }
                        } }
                    />

                    <TextField
                        { ...register( 'city' ) }
                        label="Град"
                        select
                        error={ !!errors.city }
                        helperText={ "Град на регистрация" }
                        value={ selectedCity }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedCity( event.target.value ) }
                        sx={ { textAlign: "center" } }
                    >
                        { citiesQuery.data?.map( ( city: string ) => (
                            <MenuItem key={ city } value={ city }>
                                { city }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'price' ) }
                        label="По избор: цена на автомобила"
                        type="text"
                        placeholder="Цена на автомобила"
                        error={ !!errors.price }
                        helperText={ "Цена на автомобила" }
                    />

                    <br />
                    <StyledButton type="submit" disabled={ mutation.isPending }>
                        { mutation.isPending ? <CircularProgress size={ "15rem" } /> : "Търси" }
                    </StyledButton>
                </StyledFormDesktop>

            ) }
            { carData &&
                <CarPriceResponse
                    car={ carData }
                    open={ openDialog }
                    onClose={ () => setOpenDialog( false ) }
                />
            }
            { ( mutation.isPending ) &&
                <>
                    <CircularProgress size={ "15rem" } variant="indeterminate" />
                    <StyledText>Заявката се обработва, моля изчакайте...</StyledText>
                </>
            }
            { !carData && mutation.isError &&
                <CarPriceNotFoundResponse
                    brand={ selectedCarBrand! }
                    model={ selectedModel }
                    year={ selectedYear }
                    open={ openDialog }
                    onClose={ () => setOpenDialog( false ) }
                />
            }
        </>
    );
};

export default CarDetailsForm;
