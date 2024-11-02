import * as yup from "yup";

const CarDetailsSchema = yup.object().shape( {
    brand: yup.string().min( 2 ).max( 200 ).required( "Car brand is required" ),
    model: yup.string().min( 2 ).max( 200 ).required( "Model is required" ),
    year: yup.string().min(4).max(4).required( "Year is required" ),
    fuel_type: yup.string().required( "You must specify fuel type of the car" ),
    engine_capacity: yup.string().required( "Engine capacity is required" ),
    city: yup.string().required("Specify city"),
    power_hp: yup.string().optional().nullable( "The car power in HP" ),
    power_kw: yup.string().optional().nullable( "The car power in KW" ),
    price: yup.string().optional().nullable( "Optional: price of your car" ),
} );

export default CarDetailsSchema;