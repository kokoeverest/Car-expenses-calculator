export interface Engine
{
    id: number | null;
    capacity: string;
    power_hp: string;
    power_kw: string;
    emissions_category: string;
    consumption: number | null;
    oil_capacity: string | null;
    oil_type: string | null;
}