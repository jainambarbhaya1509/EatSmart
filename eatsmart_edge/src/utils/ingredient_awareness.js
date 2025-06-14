import { ingredientSchema, IngredientsSchema } from '../schema/ingredient_awareness_schema.js';
import { loadModel } from '../main/main.js';



// ------------------------------
// Preservatives Awareness
// ------------------------------

export async function ingredientsAwareness(context, query) {
    try {
        const { model, chat } = await loadModel(context, query);

        const prediction = await model.respond(chat, {
            temperature: 0,
            structured: {
                type: "json",
                jsonSchema: ingredientSchema,
            },
        });
        const parsed = JSON.parse(prediction.content);
        const result = IngredientsSchema.safeParse(parsed);
        if (!result.success) {
            console.error("❌ Validation error:", result.error.errors);
            return null;
        }
        return result.data;

        
    } catch (error) {
        console.error("❌ Error:", error);
    }
}
