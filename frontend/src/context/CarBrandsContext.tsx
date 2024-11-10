import React, { createContext, useContext, useEffect, useState } from "react";
import carApi from "../api/carApi";
import { useQuery, useQueryClient, UseQueryResult } from "@tanstack/react-query";

const CarBrandsContext = createContext<string[]>( [] );

export const CarBrandsProvider: React.FC<{ children: React.ReactNode; }> = ( { children } ) =>
{
    const [ brandsQuery, setBrandsQuery ] = useState<string[]>( [] );

    const fetchBrands = async () =>
    {
        if (!brandsQuery) {

            try
            {
                const result: string[] = await carApi.getCarBrands();
                setBrandsQuery( result );
            }
            catch ( err )
            {
                console.error( err );
            }
        }
            
    };

    const queryClient = useQueryClient();
    const fetchBrandsV2: UseQueryResult<string[]> = useQuery<string[]>( {
        queryKey: [ "getCarBrands" ],
        queryFn: async (): Promise<string[]> => await carApi.getCarBrands()
    } );

    queryClient.invalidateQueries( { queryKey: [ 'getCarBrands' ] } );



    useEffect( () =>
    {
        fetchBrands();
    }, [] );

    return (
        <CarBrandsContext.Provider value={ fetchBrandsV2.data!}> 
        {/* <CarBrandsContext.Provider value={ brandsQuery }> */}
            { children }
        </CarBrandsContext.Provider>
    );
};

export const useCarBrands = () =>
{
    const context = useContext( CarBrandsContext );
    if ( context === undefined )
    {
        throw new Error( "useCarBrands must be used within a CarBrandsProvider" );
    }
    return context;
};