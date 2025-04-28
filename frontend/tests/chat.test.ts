import { render, screen } from "@testing-library/vue";
import userEvent from "@testing-library/user-event";
import UserInput from "@/components/chat_components/UserInput.vue";
import ChatComponent from "@/components/ChatComponent.vue";
import { vi, test, expect } from "vitest";
import { createTestingPinia } from "@pinia/testing";
import { useChatStore } from "@/stores/chat";
import ChatBubble from "@/components/chat_components/ChatBubble.vue";

test("calls function in chatView when user sends a message", async () => {
    const user = userEvent.setup();

    const assistantTriggerMock = vi.fn();

    render(ChatComponent, {
        global: {
            stubs: {
                FontAwesomeIcon: true,
            },
            plugins: [
                createTestingPinia({
                    stubActions: false,
                    createSpy: () => assistantTriggerMock,
                }),
            ],
        },
    });

    const store = useChatStore();
    const spy = vi.spyOn(store, "assistantTrigger");
    const input = screen.getByPlaceholderText("Escribe un mensaje..");
    const button = screen.getByTestId("button-send-message");

    const messages = ["Hola test", "¿Qué tiempo hace?", "Valor del dólar"];

    for (const expectedValue of messages) {
        await user.clear(input);
        await user.type(input, expectedValue);
        await user.click(button);
        expect(spy).toHaveBeenLastCalledWith(expectedValue);
    }
});

test('emits "send" event with the input message when form is submitted', async () => {
    const user = userEvent.setup();
    const { emitted } = render(UserInput, {
        global: {
            stubs: {
                FontAwesomeIcon: true,
            },
        },
    });

    const input = screen.getByPlaceholderText("Escribe un mensaje..");
    const button = screen.getByRole("button");

    await user.type(input, "Hola mundo!");
    await user.click(button);

    // assert it emitted the event
    expect(emitted().send).toBeTruthy();
    expect(emitted().send[0]).toEqual(["Hola mundo!"]);
});

test("submit button is disabled when input is empty", () => {
    render(UserInput, {
        global: {
            stubs: {
                FontAwesomeIcon: true,
            },
        },
    });
    const button = screen.getByRole("button");
    const input = screen.getByPlaceholderText("Escribe un mensaje..");
    expect(input.textContent?.length).toBe(0);
    expect(button).toBeDisabled();
});

// vite test stubs dom elements so it fails when calling .scrollIntoView
// this prevents it
window.HTMLElement.prototype.scrollIntoView = vi.fn();
test("stream-like function", async () => {
    const date = new Date();
    const message = "";
    const wrapper = render(ChatBubble, {
        props: {
            id: "test-id",
            message: message,
            fromUser: false,
            loading: true,
            timeStamp: date,
            bottomEl: document.createElement("div"),
        },
        global: {
            stubs: { FontAwesomeIcon: true },
        },
    });

    // changing the loading state will trigger the watcher
    const newMessage = "This is the updated message!";
    await wrapper.rerender({
        message: newMessage,
        loading: false,
    });

    // waits for the stream-like function to write
    await new Promise((resolve) => setTimeout(resolve, 500));

    // checks change in content length
    const expectedValue: number =
        newMessage.length + date.toLocaleTimeString().length + 1;

    const bubble = screen.getByTestId("chat-bubble");
    expect(bubble.textContent?.length ?? 0).toBe(expectedValue);
});
