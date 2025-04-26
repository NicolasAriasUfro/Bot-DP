import { beforeAll, beforeEach, expect, test, vi } from "vitest";
import { mount } from "@vue/test-utils";
import HomeView from "@/views/HomeView.vue";
import { createTestingPinia } from "@pinia/testing";
import { useChatStore } from "@/stores/chat";
import { API_ROUTE } from "@/utils/consts";

vi.mock("axios");
import axios from "axios";
import { setActivePinia } from "pinia";

test("calls pinia assistantTrigger", async () => {
    const wrapper = mount(HomeView, {
        global: {
            plugins: [createTestingPinia({ stubActions: false })],
        },
    });

    const store = useChatStore();
    const expectedValue = "message send by user";

    store.assistantTrigger(expectedValue);
    expect(store.assistantTrigger).toHaveBeenCalledTimes(1);
});

test("assistantTrigger does POST", async () => {
    const wrapper = mount(HomeView, {
        global: {
            plugins: [createTestingPinia({ stubActions: false })],
        },
    });

    const store = useChatStore();
    const expectedValue = "message send by user";

    store.assistantTrigger(expectedValue);
    expect(axios.post).toHaveBeenCalled();
});

test("creates new bot loading message", async () => {
    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const store = useChatStore();

    const expectedLength: number = 1;
    const expectedLoadingValue: boolean = true;

    // messages should be empty on load
    expect(store.messages.length).toBe(0);

    // adds loading message
    store.addBotLoadingMessage();

    // checks new message
    expect(store.messages.length).toBe(expectedLength);

    // checks loading value
    expect(store.messages[0].loading).toBe(expectedLoadingValue);
});

test("adds messages", async () => {
    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const store = useChatStore();

    const exampleMessages = [
        { message: "Hola, quiero pedir unas papas fritas.", fromUser: true },
        {
            message:
                "¡Perfecto! Tenemos papas fritas clásicas, con queso cheddar, o con tocino y salsa especial. Todas vienen en tamaño individual o para compartir. ¿Cuál prefieres?",
            fromUser: false,
        },
        {
            message: "Las clásicas están bien. ¿Cuánto cuestan las grandes?",
            fromUser: true,
        },
    ];

    const expectedValue: number = exampleMessages.length;

    exampleMessages.forEach((msg) => store.addMessage(msg));

    expect(store.messages.length).toBe(expectedValue);

});

test("empties chat messages", async () => {
    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const store = useChatStore();

    const exampleMessages = [
        { message: "Hola, quiero pedir unas papas fritas.", fromUser: true },
        {
            message:
                "¡Perfecto! Tenemos papas fritas clásicas, con queso cheddar, o con tocino y salsa especial. Todas vienen en tamaño individual o para compartir. ¿Cuál prefieres?",
            fromUser: false,
        },
        {
            message: "Las clásicas están bien. ¿Cuánto cuestan las grandes?",
            fromUser: true,
        },
    ];

    exampleMessages.forEach((msg) => store.addMessage(msg));

    const expectedValue: number = 0;

    // checks current messages length
    expect(store.messages.length).toBe(3);

    // clears messages
    store.clearChat();

    expect(store.messages.length).toBe(expectedValue);
});
