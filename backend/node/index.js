// server.js or index.js
import express from 'express';
import {
  preservativesAwarenessContext,
  homemadeHealthyAlternativeContext,
  ocrScannerContext,
  chatbotContext,
  heightEstimationContext,
  cookedFoodContext,
} from './context/contexts.js';

import { homemadeAlternatives } from './utils/homemade_alternatives.js';
import { ocrAnalysis } from './utils/ocr_analysis.js';
import { healthcareChatbot, newChat } from './utils/health_chatbot.js';

import OpenFoodFacts from "openfoodfacts-nodejs";
import multer from 'multer';
import { ingredientsAwareness } from './utils/ingredient_awareness.js';
import { heightEstimation } from './utils/height_estimation.js';
import { cookedFoodAnalysis } from './utils/cooked_food_analysis.js';

const app = express();
app.use(express.json());
const PORT = 3000;
const upload = multer({ dest: 'uploads/' });

// ------------------------------
// API Call
// ------------------------------

app.get('/barcode-scan/:code', async (req, res) => {
  const code = req.params.code;
  try {
    const client = new OpenFoodFacts();
    const result = await client.getProduct(code);
    console.log(result);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to analyze preservative.', details: err.message });
  }
});


// ------------------------------
// EDGE AI Features
// ------------------------------

app.get('/ingredients/:code', async (req, res) => {
  const code = req.params.code;
  try {
    const result = await ingredientsAwareness(preservativesAwarenessContext, code)
    console.log(result);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to analyze preservative.', details: err.message });
  }
});


app.get('/homemade-alternative/:item', async (req, res) => {
  const item = req.params.item;
  try {
    const result = await homemadeAlternatives(homemadeHealthyAlternativeContext, item);
    console.log(result);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to generate homemade alternative.', details: err.message });
  }
});

app.get("/chat/:userQuery", async (req, res) => {
  const userQuery = decodeURIComponent(req.params.userQuery);

  try {
    const response = await healthcareChatbot(
      chatbotContext,
      userQuery
    );
    res.json({ response });
  } catch (err) {
    console.error("❌ Route Error:", err);
    res.status(500).json({
      error: "Failed to respond",
      details: err.message,
    });
  }
});

app.get("/reset", (req, res) => {
  newChat(chatbotContext);
  res.json({ message: "🔄 Chat history reset." });
});


app.post('/ocr-analysis', upload.single('image'), async (req, res) => {
  try {
    const imagePath = req.file.path;
    const result = await ocrAnalysis(ocrScannerContext, imagePath);
    console.log(result);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to perform OCR.', details: err.message });
  }
});

app.post('/cooked-food-analysis', upload.single('image'), async (req, res) => {
  try {
    const imagePath = req.file.path;
    const result = await cookedFoodAnalysis(cookedFoodContext, "Which food is in the image", imagePath);
    console.log(result);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to perform OCR.', details: err.message });
  }
});

app.post('/height-estimation', upload.single('image'), async (req, res) => {
  try {
    const imagePath = req.file.path;
    const result = await heightEstimation(heightEstimationContext, "What is the height of the person (X Feet Y Inch) wrt the distance from the phone and surroundings ?" ,imagePath);
    console.log(result);
    res.json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to perform OCR.', details: err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
