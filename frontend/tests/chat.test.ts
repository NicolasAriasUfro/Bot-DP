import { render, screen } from "@testing-library/vue";
import userEvent from "@testing-library/user-event";
import UserInput from "@/components/chat_components/UserInput.vue";
import ChatComponent from "@/components/ChatComponent.vue";
import { vi, test, expect } from "vitest";
import { createTestingPinia } from "@pinia/testing";
import { useChatStore } from "@/stores/chat";

test("calls function in chat when user sends a message", async () => {
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
    const button = screen.getByRole("button");

    await user.type(input, "Hola test");
    await user.click(button);

    expect(spy).toHaveBeenCalledWith("Hola test");
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
    expect(button).toBeDisabled();
});
