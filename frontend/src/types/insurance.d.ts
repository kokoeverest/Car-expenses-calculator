export interface Insurance
{
    id: number;
    year: string;
    engine_size: string;
    fuel_type: string;
    power: string;
    municipality: string;
    registration: bool;
    driver_age: string | null;
    driving_experience: string;
    min_price: number;
    max_price: number;
    date: Date | null;
}