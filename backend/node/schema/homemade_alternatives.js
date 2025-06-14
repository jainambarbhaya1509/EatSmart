import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

export const HomemadeHealthyAlternativeSchema = z.object({
  alternative_name: z.string().describe("Creative name for the homemade alternative"),
  
  description: z.string().describe("Brief explanation of the recipe and its purpose"),
  
  ingredients: z.array(
    z.object({
      name: z.string().describe("Name of the ingredient"),
      quantity: z.string().describe("Amount and unit (e.g., '1 cup', '2 tsp')"),
      optional: z.boolean().optional().describe("Whether the ingredient is optional")
    })
  ).describe("List of ingredients with quantity and optional flag"),
  
  instructions: z.array(
    z.string().describe("Step-by-step preparation instruction")
  ).describe("Cooking or preparation steps"),
  
  health_benefits: z.array(
    z.string().describe("Health advantages of this alternative over the packaged item")
  ).describe("List of nutritional and health benefits"),
  
  suitable_for: z.array(
    z.string().describe("Groups of people for whom this recipe is particularly beneficial (e.g., children, diabetics)")
  ).optional().describe("Target groups who benefit most from this alternative"),
  
  storage_info: z.string().optional().describe("Storage recommendations, if applicable"),
  
  cultural_reference: z.string().optional().describe("Optional mention of traditional/cultural basis or Ayurvedic value, if any")
});

export const homefoodAlt = zodToJsonSchema(HomemadeHealthyAlternativeSchema, "HomemadeHealthyAlternativeSchema");