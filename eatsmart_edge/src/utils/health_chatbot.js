import { Chat } from "@lmstudio/sdk";
import { loadModel } from "../main/main.js";


// Initialize global chat storage if it doesn't exist
globalThis.allChats = globalThis.allChats || [];

// Function to get latest chat (or create new if none)
export function getLastChat(context) {
    if (globalThis.allChats.length === 0) {
        const chat = Chat.from([]);
        chat.append("system", context);
        globalThis.allChats.push(chat);
    }

    return globalThis.allChats[globalThis.allChats.length - 1];
}

// Optional: Add a new chat if you want to restart
export function newChat(context) {
    const chat = Chat.from([]);
    chat.append("system", context);
    globalThis.allChats.push(chat);
    return chat;
}

export async function healthcareChatbot(context, userMessage) {
    try {
        const { model } = await loadModel();
        const chat = getLastChat(context);

        chat.append("user", userMessage);

        let assistantContent = "";

        const prediction = await model.respond(chat, {
            onMessage: (message) => {
                assistantContent += message.content || "";
                chat.append("assistant", message.content || "");
            },
        });

        return prediction.content;

    } catch (error) {
        console.error("❌ Error:", error);
        return "An error occurred. Please try again later.";
    }
}
