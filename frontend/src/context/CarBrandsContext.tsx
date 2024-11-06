import React, { createContext, useContext, useEffect, useState } from "react";
import carApi from "../api/carApi";

const CarBrandsContext = createContext<string[] | null>( null );

export const CarBrandsProvider: React.FC<{ children: React.ReactNode; }> = ( { children } ) =>
{
    const [brandsQuery, setBrandsQuery] = useState<string[] | null>(null);

    const fetchBrands = async () =>
        {
            try
            {
                const result: string[] = await carApi.getCarBrands();
                setBrandsQuery(result);
            }
            catch (err)
            {
                console.error(err)
            }
            
     };

     useEffect(() =>
    {
        fetchBrands();
    }, [] );

    return (
        <CarBrandsContext.Provider value={ brandsQuery }>
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