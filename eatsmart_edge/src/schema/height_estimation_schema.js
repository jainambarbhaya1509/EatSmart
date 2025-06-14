import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';


export const HeightEstSchema = z.object({
  height: z.string()
});

export const heightSchema = zodToJsonSchema(HeightEstSchema, "HeightEstSchema");
