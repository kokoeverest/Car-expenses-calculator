import { AxiosResponse } from "axios";
import { BASE_URL, API_ENUMS_BASE_URL } from "../common/constants";
import { CarDetailFormInput } from "../features/abstract";
import { Car } from "../types/car";
import { api } from "./api";

const carApi = {

    getCarPrice: async ( data: CarDetailFormInput ): Promise<Car> =>
    {
        const response: AxiosResponse = await api.post( `${ BASE_URL }/`, data, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        } );
        console.log( "Response data:\n", response.data );
        return response.data;
    },

    getCarBrands: async (): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_ENUMS_BASE_URL }/brands` );
        return response.data;
    },

    getModels: async ( brand: string ): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_ENUMS_BASE_URL }/${ brand }/models` );
        return response.data;
    },

    getModelYears: async ( brand: string, model: string ): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_ENUMS_BASE_URL }/${ brand }/${ model }/years` );
        return response.data;
    },

    getCities: async (): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_ENUMS_BASE_URL }/cities` );
        return response.data;
    }

};
export default carApi;