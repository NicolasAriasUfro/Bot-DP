import { expect, test, vi } from "vitest";
import { mount } from "@vue/test-utils";
import HomeView from "@/views/HomeView.vue";
import { createTestingPinia } from "@pinia/testing";
import { useChatStore } from "@/stores/chat";
import { API_ROUTE } from "@/utils/consts";

vi.mock("axios");
import axios from "axios";

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
    expect(axios.post).toHaveBeenCalled();
});
