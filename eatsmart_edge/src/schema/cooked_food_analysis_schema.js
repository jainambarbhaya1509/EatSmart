import { z } from "zod";
import { zodToJsonSchema } from 'zod-to-json-schema';


export const FoodAnalysisSchema = z.object({
  foodName: z.string().min(1),
  foodType: z.enum(["Junk Food", "Homemade", "Fast Food", "Processed", "Other"]),
  nutritionalInfo: z.object({
    calories: z.number().min(0),
    carbohydrates: z.number().min(0),
    protein: z.number().min(0),
    fat: z.number().min(0),
    sugar: z.number().min(0),
    sodium: z.number().min(0),
  }),
  healthRisks: z.array(z.string()).optional(),
  healthSuggestions: z.array(z.string()).optional(),
});


export const cookedFoodSchema = zodToJsonSchema(FoodAnalysisSchema, "FoodAnalysisSchema");
