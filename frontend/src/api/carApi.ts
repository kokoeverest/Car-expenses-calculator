import { AxiosResponse } from "axios";
import { API_BASE_URL } from "../common/constants";
import { CarDetailFormInput } from "../features/abstract";
import { Car } from "../types/car";
import { api } from "./api";

const carApi = {

    getCarPrice: async ( data: CarDetailFormInput ): Promise<Car> =>
    {
        const response: AxiosResponse = await api.post( `${ API_BASE_URL }/`, data, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        } );

        return response.data;
    },

    getCarBrands: async (): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_BASE_URL }/brands` );
        return response.data;
    },

    getModels: async ( brand: string ): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_BASE_URL }/${ brand }/models` );
        return response.data;
    },

    getCities: async (): Promise<string[]> =>
    {
        const response: AxiosResponse<string[]> = await api.get<string[]>( `${ API_BASE_URL }/cities` );
        return response.data;
    }

};
export default carApi;