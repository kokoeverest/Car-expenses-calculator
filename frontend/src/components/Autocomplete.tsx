import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import carApi from '../api/carApi';
import { useQuery, UseQueryResult } from '@tanstack/react-query';

export default function ComboBox ()
{
const brandsQuery: UseQueryResult<string[], Error> = useQuery( {
    queryKey: [ 'getCities' ],
    queryFn: carApi.getCities,
} );

    return (
        <Autocomplete
            // disablePortal
            options={ brandsQuery.data! }
            // sx={ { width: "justify" } }
            renderInput={ ( params ) => <TextField { ...params } label="Cities" /> }
        />
    );
}