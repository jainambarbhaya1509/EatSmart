import { loadModel } from '../main/main.js';
import { homefoodAlt, HomemadeHealthyAlternativeSchema } from '../schema/homemade_alternatives.js';


// ------------------------------
// Homemade Alternatives
// ------------------------------

export async function homemadeAlternatives(context, query) {
    try {
        const { model, chat } = await loadModel(context, query);

        const prediction = await model.respond(chat, {
            temperature: 0,
            structured: {
                type: "json",
                jsonSchema: homefoodAlt,
            },
        });
        const parsed = JSON.parse(prediction.content);
        // Zod validation
        const result = HomemadeHealthyAlternativeSchema.safeParse(parsed);
        if (!result.success) {
            console.error("❌ Validation error:", result.error.errors);
            return null;
        }
        return result.data;

    } catch (error) {
        console.error("❌ Error:", error);
    }
}
