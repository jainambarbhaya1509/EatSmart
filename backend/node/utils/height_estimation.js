import { loadImageModel } from '../main/main.js';
import { HeightEstSchema, heightSchema } from '../schema/height_estimation_schema.js';



// ------------------------------------------------
// Height Estimation -- Customer Retention Feature
// ------------------------------------------------

export async function heightEstimation(context, query, imgPath) {
    try {
        const { model, chat } = await loadImageModel(context, query, imgPath);

        const prediction = await model.respond(chat, {
            structured: {
                type: "json",
                jsonSchema: heightSchema,
            },
        });
        
        const parsed = JSON.parse(prediction.content);
        const result = HeightEstSchema.safeParse(parsed);
        
        if (!result.success) {
            console.error("❌ Validation error:", result.error.errors);
            return null;
        }

        return result.data
    } catch (error) {
        console.error("❌ Error:", error);
    }
}
