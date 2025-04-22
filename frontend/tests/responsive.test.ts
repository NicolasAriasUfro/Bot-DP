import ChatComponent from "@/components/ChatComponent.vue";
import { expect, test } from "vitest";
import { render, screen } from "@testing-library/vue";
import { createTestingPinia } from "@pinia/testing";
import { beforeEach } from "node:test";
import ChatView from "@/views/ChatView.vue";
import ChatBubble from "@/components/chat_components/ChatBubble.vue";
import UserInput from "@/components/chat_components/UserInput.vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

test("renders mobile layout under 640px", async () => {
    window.innerWidth = 500;
    window.dispatchEvent(new Event("resize"));

    render(ChatView, {
        global: {
            stubs: {},
            components: { ChatComponent, ChatBubble, FontAwesomeIcon },
            plugins: [createTestingPinia()],
        },
    });
    render(ChatBubble);

    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("chat-bubble")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});

test("renders desktop layout under 1024px", async () => {
    window.innerWidth = 1000;
    window.dispatchEvent(new Event("resize"));

    render(ChatView, {
        global: {
            stubs: {},
            components: {
                ChatComponent,
                ChatBubble,
                UserInput,
                FontAwesomeIcon,
            },
            plugins: [createTestingPinia()],
        },
    });
    render(ChatBubble);

    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("chat-bubble")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});
