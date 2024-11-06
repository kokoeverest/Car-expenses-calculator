import { Engine } from "./engine";
import { Tax } from "./tax";
import { Tire } from "./tire";
import { Insurance } from "./insurance";

export interface Car
{
    id: number;
    brand: string;
    model: string;
    year: string;
    engine: Engine;
    tax: Tax;
    tires: Tire[];
    price: string;
    insurance: Insurance;
    vignette: number;
    seats: number;
}