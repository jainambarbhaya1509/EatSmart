import { z } from 'zod';
import { zodToJsonSchema } from 'zod-to-json-schema';

export const IngredientsSchema = z.object({
  additive_info: z.object({
    common_name: z.string(),
    chemical_name: z.string(),
    chemical_code: z.string(),
    category: z.string(),
    usages: z.array(
      z.object({
        role: z.string(),
        purpose: z.string()
      })
    ),
    properties: z.object({
      brightness: z.string(),
      stability: z.string(),
      cost_efficiency: z.string()
    }),
    health_profile: z.object({
      safety: z.object({
        status: z.string(),
        evaluated_by: z.string(),
        year: z.number()
      }),
      potential_risks: z.object({
        environmental: z.string(),
        vulnerable_groups: z.array( 
          z.object({
            group: z.string(),  
            effect: z.string()
          })
        ),
        digestive_effect: z.string(),
        long_term_effect: z.string(),
        metabolism_effect: z.string()
      })
    }),
    regulatory_status: z.object({
      acceptable_daily_intake: z.object({
        value_mg_per_kg_bw: z.string(),
        source: z.string()
      }),
      country_regulations: z.array(
        z.object({
          region: z.string(),
          status: z.string(),
          note: z.string()
        })
      ),
      global_regulatory_bodies: z.array(  // new addition for FDA/EFSA/WHO alignment
        z.object({
          body: z.string(),        // e.g., "FDA", "EFSA", "WHO"
          evaluation: z.string(),  // e.g., "Approved", "Restricted"
          status: z.string()       
        })
      )
    }),
    alternatives: z.array(
      z.object({
        name: z.string(),
        code: z.string()
      })
    ),
    scientific_references: z.array(
      z.object({
        title: z.string(),
        organization: z.string(),
        year: z.number(),
        type: z.string() // e.g., "Journal Article", "WHO Report"
      })
    )
  })
});

export const ingredientSchema = zodToJsonSchema(IngredientsSchema, "PreservativeSchema");