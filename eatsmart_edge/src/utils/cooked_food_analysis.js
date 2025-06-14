import { loadImageModel } from '../main/main.js';
import { cookedFoodSchema, FoodAnalysisSchema } from '../schema/cooked_food_analysis_schema.js';

// ------------------------------------------------
// Cooked Food/Junk Food Analysis
// ------------------------------------------------

export async function cookedFoodAnalysis(context, imgPath) {
    try {
        const { model, chat } = await loadImageModel(context, imgPath);

        const prediction = await model.respond(chat, {
            structured: {
                type: "json",
                jsonSchema: cookedFoodSchema,
            },
        });
        
        const parsed = JSON.parse(prediction.content);
        const result = FoodAnalysisSchema.safeParse(parsed);
        
        if (!result.success) {
            console.error("❌ Validation error:", result.error.errors);
            return null;
        }

        return result.data
    } catch (error) {
        console.error("❌ Error:", error);
    }
}
