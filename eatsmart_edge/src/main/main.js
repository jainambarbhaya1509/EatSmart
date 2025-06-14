import { LMStudioClient, Chat } from "@lmstudio/sdk";

// ----------------------------------------------------------------------------
// LMStudioClient
// ----------------------------------------------------------------------------

const client = new LMStudioClient();

export async function loadModel(context, query) {

  const model = (await client.llm.model("google/gemma-3-4b"));
  let chat = Chat.from([
    { role: "system", content: context },
    { role: "user", content: query },
  ]);
  return { model, chat };
}

export async function loadImageModel(context, query, imagePath) {

  const model = (await client.llm.model("google/gemma-3-4b"));
  const image = await client.files.prepareImage(imagePath);

  let chat = Chat.from([
    { role: "system", content: context },
    { role: "user", content: query, images: [image] },
  ]);



  return { model, chat };
}

export async function loadOCRModel(context, imagePath) {

  const model = (await client.llm.model("nanonets-ocr-s"));
  const image = await client.files.prepareImage(imagePath);
  let chat = Chat.from([
    { role: "system", content: context },
    { role: "user", images: [image] },
  ]);

  return { model, chat };
}

export async function loadChatbotModel() {
  const chat = new Chat();
  const model = await client.llm.chat({ model: "google/gemma-3-4b" });

  return { model, chat };
}