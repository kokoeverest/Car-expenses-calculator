export interface CarDetailFormInput 
{
    brand: string;
    model: string;
    year: string;
    fuel_type: string;
    engine_capacity: string;
    city: string;
    power_hp?: string | null;
    power_kw?: string | null;
    price?: string | null;
}