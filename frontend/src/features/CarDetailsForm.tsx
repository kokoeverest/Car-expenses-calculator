import React, { useEffect, useState } from "react";
import { useForm, SubmitHandler } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useNavigate } from "react-router-dom";
import { CircularProgress, MenuItem, TextField } from "@mui/material";
import { useMutation, UseMutationResult, useQuery, useQueryClient, UseQueryResult } from "@tanstack/react-query";
import StyledButton from "../components/controls/StyledButton";
import StyledForm from "../components/controls/StyledForm";
import { CarDetailFormInput } from "./abstract";
import carApi from "../api/carApi";
import CarDetailsSchema from "./schemas";
import { Car } from "../types/car";

const CarDetailsForm: React.FC = () =>
{
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const [ selectedCarBrand, setSelectedCarBrand ] = useState( 'Audi' );
    const [ selectedModel, setSelectedModel ] = useState( 'a1' );
    const [ selectedCity, setSelectedCity ] = useState( 'София' );
    const [ selectedFuelType, setSelectedFuelType ] = useState( 'diesel' );

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
        queryFn: (): Promise<string[]> => carApi.getModels( selectedCarBrand ),
        enabled: !!selectedCarBrand,
    } );

    const brandsQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ 'getCarBrands' ],
        queryFn: carApi.getCarBrands,
    } );

    const citiesQuery: UseQueryResult<string[], Error> = useQuery( {
        queryKey: [ 'getCities' ],
        queryFn: carApi.getCities,
    } );

    const mutation: UseMutationResult<Car, Error, CarDetailFormInput, unknown> = useMutation( {
        mutationFn: carApi.getCarPrice,
        onSuccess: (): void =>
        {
            alert( "Successful! Thank you!" );
            // navigate( "/" );
            queryClient.invalidateQueries( { queryKey: [ 'getCarBrands', 'getCarModels', 'getCities' ] } );
        },
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
            { !mutation.isError && !mutation.isPending && !carModelsQuery.isPending && (
                <StyledForm onSubmit={ handleSubmit( onSubmitHandler ) }>
                    <h1>Enter the car data</h1>

                    <TextField
                        { ...register( "brand" ) }
                        select
                        label="Select car brand"
                        error={ !!errors.brand }
                        helperText={ errors.brand?.message }
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
                        value={ "2024" }
                        helperText={ "Select the year of the car" }
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
                </StyledForm>
            ) }

            { mutation.isError && <h3>Error</h3> }
            { ( carModelsQuery.isPending || mutation.isPending ) && <CircularProgress size={ "15rem" } variant="indeterminate" /> }
        </>
    );
};

export default CarDetailsForm;
