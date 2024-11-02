import axios from "axios";
import { API_BASE_URL } from "../common/constants";

const api = axios.create( {
    baseURL: API_BASE_URL,
    withCredentials: false
} );

api.interceptors.response.use( ( response ) => response, ( error ) =>
{
    if ( !error.response )
    {
        console.log( 'Network error:', error );
        return Promise.reject( error );
    }

    switch ( error.response.status )
    {
        case 404:
            console.log( "Not found response!" );
            break;
        case 403:
            console.log( 'Forbidden!' );
            break;
        case 401:
            console.log( "Unauthorized!" );
            break;
        default: console.log( error.response.data );
    }

    return Promise.reject( error );
} );

export { api };