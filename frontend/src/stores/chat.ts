import type { AssistantResponse, ChatMessage } from "@/utils/types";
import { defineStore } from "pinia";
import axios from "axios";
import { API_ROUTE } from "@/utils/consts";

export const useChatStore = defineStore("chat", {
    state: () => ({
        messages: [] as ChatMessage[],
        loading: false,
    }),
    actions: {
        async assistantTrigger(newMessage: string) {
            console.info("ASSISTANT_TRIGGER WAS CALLED");
            this.loading = true;
            try {
                const headers = {};
                const url = `${API_ROUTE}/assistant/query`;
                const data = {
                    message: newMessage,
                };
                const response = await axios.post(url, data, {
                    headers,
                });

                // gets response and parses it
                const assistantMessage: AssistantResponse = {
                    message: response.data.response,
                };

                console.info("message received: ", assistantMessage.message);

                // TODO: REMOVE THIS ON PROD
                // const test_message = `There's something magical about the way a warm,
                //     homemade meal can bring people together — the aroma of garlic sizzling in olive oil,
                //     the comforting steam rising from a bowl of freshly made pasta, or the satisfying crunch of a well-seasoned roasted vegetable.
                //     Food isn’t just nourishment; it’s tradition, culture, and memory served on a plate.
                //     Whether it’s a slow-cooked stew passed down through generations or an experimental
                //     fusion taco from a food truck, each bite tells a story. And often, the best conversations and connections
                //     happen not in the living room or office, but around a kitchen table, over a shared love for something delicious.`;

                // last message is currently loading
                // update the last message with the one we got
                this.handleAssistantResponse(assistantMessage);

            } catch (why) {
                console.error("Could not get bot response: ", why);
            } finally {
                this.loading = false;
            }
        },

        /**
         * Updates the last and currently loading message
         * 
         * @param assistantMessage 
         */
        handleAssistantResponse(assistantMessage: AssistantResponse) {
            if (this.messages.length > 0) {
                const lastIndex = this.messages.length - 1;
                this.messages[lastIndex] = {
                    ...this.messages[lastIndex],
                    message: assistantMessage.message,
                    loading: false,
                    timestamp: new Date(),
                };
            }
        },


        /**
         * Adds a message to the list of messages in the store
         * 
         * @param message 
         */
        addMessage(message: Omit<ChatMessage, "id" | "timestamp" | "loading">) {
            const newMsg: ChatMessage = {
                id: crypto.randomUUID(),
                timestamp: new Date(),
                loading: false,
                ...message,
            };
            this.messages.push(newMsg);
        },

        /**
         * Adds one bot loading message,
         * use this while waiting for the assistant response 
         */
        addBotLoadingMessage() {
            const newMsg: ChatMessage = {
                id: crypto.randomUUID(),
                timestamp: new Date(),
                loading: true,
                message: "",
                fromUser: false,
            };
            this.messages.push(newMsg);
        },

        /**
         * Clears the whole chat
         */
        clearChat() {
            this.messages = [];
        },
    },
    persist: true,
});
