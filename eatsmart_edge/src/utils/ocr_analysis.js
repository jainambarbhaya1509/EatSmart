import { loadOCRModel } from '../main/main.js';
import { ocrFoodAnalysis, OCRFoodAnalysisSchema } from '../schema/ocr_ingredients_schema.js';


// ------------------------------
// OCR Model - Image to Text
// ------------------------------

export async function ocrAnalysis(context, imgPath) {
    try {
        const { model, chat } = await loadOCRModel(context, imgPath);

        const prediction = await model.respond(chat, {
            structured: {
                type: "json",
                jsonSchema: ocrFoodAnalysis,
            },
        });
        const parsed = JSON.parse(prediction.content);
        const result = OCRFoodAnalysisSchema.safeParse(parsed);
        
        if (!result.success) {
            console.error("❌ Validation error:", result.error.errors);
            return null;
        }

        return result.data
    } catch (error) {
        console.error("❌ Error:", error);
    }
}
