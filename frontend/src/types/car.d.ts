import { Engine } from "./engine";
import { Tax } from "./tax";
import { Tire } from "./tire";
import { Insurance } from "./insurance";

export interface Car
{
    id: number | null;
    brand: string;
    model: string;
    year: string;
    engine: Engine | null;
    tax: Tax | null;
    tires: Array<Tire> | string;
    price: string;
    insurance: Insurance | number | null;
    vignette: number;
    seats: number;
}