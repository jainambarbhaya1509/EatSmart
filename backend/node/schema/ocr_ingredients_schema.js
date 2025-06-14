import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';


export const OCRFoodAnalysisSchema = z.object({
    list_of_ingredients: z.array(z.string()),
    nutrition_facts: z.array(
        z.object({
            key: z.string(),
            value: z.string()
        })
    )
});


export const ocrFoodAnalysis = zodToJsonSchema(OCRFoodAnalysisSchema, "OCRFoodAnalysisSchema");