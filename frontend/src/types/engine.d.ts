import { Fuel } from "./fuel";

export interface Engine
{
    id: number;
    capacity: string;
    power_hp: string;
    power_kw: string;
    fuel: Fuel;
    emissions_category: string;
    consumption: number;
    oil_capacity: string | null;
    oil_type: string | null;
}