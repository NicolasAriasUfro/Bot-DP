import type { ChatMessage } from "@/utils/types";
import { defineStore } from "pinia";
import axios from "axios";
import { API_ROUTE } from "@/utils/consts";

export const useChatStore = defineStore("chat", {
    state: () => ({
        messages: [] as ChatMessage[],
        loading: false,
    }),
    actions: {
        async loadMessages() {
            this.loading = true;
            try {
                // TODO: UPDATE
                const headers = {};
                const response = await axios.get(
                    `${API_ROUTE}/api/larutadelnico`,
                    {
                        headers,
                    }
                );

                this.messages = response.data.map((msg: any) => ({
                    ...msg,
                    timestamp: new Date(msg.timestamp),
                }));
            } catch (why) {
                console.error("Failed to load messages", why);
            } finally {
                this.loading = false;
            }
        },

        async saveUserMessage(newMessage: string) {
            this.loading = true;
            try {
                // TODO: UPDATE
                const headers = {};
                const response = await axios.get(
                    `${API_ROUTE}/api/larutadelnico`,
                    {
                        headers,
                    }
                );

                this.messages = response.data.map((msg: any) => ({
                    ...msg,
                    timestamp: new Date(msg.timestamp),
                }));
            } catch (why) {
                console.error("Failed to load messages", why);
            } finally {
                this.loading = false;
            }
        },

        addMessage(message: Omit<ChatMessage, "id" | "timestamp" | "loading">) {
            const newMsg: ChatMessage = {
                id: crypto.randomUUID(),
                timestamp: new Date(),
                loading: false,
                ...message,
            };
            this.messages.push(newMsg);
        },
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

        clearChat() {
            this.messages = [];
        },
    },
    persist: true,
});
