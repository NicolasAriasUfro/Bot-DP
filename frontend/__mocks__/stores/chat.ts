import { vi } from "vitest";

export const saveUserMessage = vi.fn()
export const addMessage = vi.fn()
export const addBotLoadingMessage = vi.fn()
export const clearChat = vi.fn()

export const useChatStore = vi.fn(() => ({
    messages: [],
    loading: false,
    saveUserMessage: vi.fn(),
    addMessage: vi.fn(),
    addBotLoadingMessage: vi.fn(),
    clearChat: vi.fn(),
}));
