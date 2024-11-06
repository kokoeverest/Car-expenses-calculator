import React, { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { CircularProgress, MenuItem, TextField } from "@mui/material";
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
import { useCarBrands } from "../context/CarBrandsContext";

const CarDetailsForm: React.FC = () =>
{
    const carBrands = useCarBrands();
    const queryClient = useQueryClient();
    const [ selectedCarBrand, setSelectedCarBrand ] = useState<string | null>( null );
    const [ selectedModel, setSelectedModel ] = useState( '' );
    const [ selectedCity, setSelectedCity ] = useState( '' );
    const [ selectedFuelType, setSelectedFuelType ] = useState( 'diesel' );
    const [ selectedYear, setSelectedYear ] = useState( '2015' );
    const [ openDialog, setOpenDialog ] = useState( false );
    const [ carData, setCarData ] = useState<Car | null>( null );


    const fuel_types: string[] = [
        "eev",
        "gasoline",
        "diesel",
        "lpg",
        "methane",
    ];

    const getYears: () => number[] = (): number[] =>
    {
        const result: number[] = [];
        for ( let i: number = 2024; i >= 1970; i-- )
        {
            result.push( i );
        }
        return result;
    };

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<CarDetailFormInput>( {
        resolver: yupResolver( CarDetailsSchema ),
    } );


    const carModelsQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ "getCarModels", selectedCarBrand ],
        queryFn: (): Promise<string[]> => carApi.getModels( selectedCarBrand! ),
        // enabled: selectedCarBrand == null,
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
            queryClient.invalidateQueries( { queryKey: [ 'getCarModels', 'getCities' ] } );
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

    return (
        <>
            { !mutation.isPending && !carModelsQuery.isPending && (
                <StyledFormDesktop onSubmit={ handleSubmit( onSubmitHandler ) }>
                    <StyledText variant="h4">Enter the car data</StyledText>

                    <TextField
                        { ...register( "brand" ) }
                        select
                        label="Select car brand"
                        error={ !!errors.brand }
                        helperText={ errors.brand?.message }
                        value={ selectedCarBrand }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedCarBrand( event.target.value ) }
                    >
                        { carBrands?.map( ( brand: string ) => (
                            <MenuItem key={ brand } value={ brand }>
                                { brand }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'model' ) }
                        select
                        label="Select model"
                        error={ !!errors.model }
                        helperText={ errors.model?.message }
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
                        label="Year"
                        error={ !!errors.year }
                        value={ selectedYear }
                        helperText={ "Select the year of the car" }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedYear( event.target.value ) }
                    >
                        { getYears().map( ( year: number ) => (
                            <MenuItem key={ year } value={ year }>
                                { year }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'fuel_type' ) }
                        label="Fuel type"
                        select
                        error={ !!errors.fuel_type }
                        helperText={ "Select fuel type of the car" }
                        value={ selectedFuelType }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedFuelType( event.target.value ) }
                    >
                        { fuel_types.map( ( fuelType: string ) => (
                            <MenuItem key={ fuelType } value={ fuelType }>
                                { fuelType }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'engine_capacity' ) }
                        label="Engine capacity"
                        type="text"
                        error={ !!errors.engine_capacity }
                        helperText={ "Capacity of the engine" }
                    />

                    <TextField
                        { ...register( 'city' ) }
                        label="City"
                        select
                        error={ !!errors.city }
                        helperText={ "City of registration" }
                        value={ selectedCity }
                        onChange={ ( event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement> ): void => setSelectedCity( event.target.value ) }
                    >
                        { citiesQuery.data?.map( ( city: string ) => (
                            <MenuItem key={ city } value={ city }>
                                { city }
                            </MenuItem>
                        ) ) }
                    </TextField>

                    <TextField
                        { ...register( 'power_hp' ) }
                        label="Engine power in HP"
                        type="text"
                        error={ !!errors.power_hp }
                        helperText={ "Engine power in HP" }
                    />

                    <TextField
                        { ...register( 'power_kw' ) }
                        label="Engine power in KW"
                        type="text"
                        placeholder="Engine power in KW"
                        error={ !!errors.power_kw }
                        helperText={ "Engine power in KW" }
                    />

                    <TextField
                        { ...register( 'price' ) }
                        label="Optional: price of the car"
                        type="text"
                        placeholder="Car price"
                        error={ !!errors.price }
                        helperText={ "Car price" }
                    />

                    <br />
                    <StyledButton type="submit" disabled={ mutation.isPending }>
                        { mutation.isPending ? <CircularProgress size={ "15rem" } /> : "Submit" }
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
            { ( carModelsQuery.isPending || mutation.isPending ) &&
                <>
                    <CircularProgress size={ "15rem" } variant="indeterminate" />
                    <StyledText>Collecting car prices, please wait...</StyledText>
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
