import ChatComponent from "@/components/ChatComponent.vue";
import { expect, test } from "vitest";
import { render, screen } from "@testing-library/vue";
import { createTestingPinia } from "@pinia/testing";
import ChatView from "@/views/ChatView.vue";
import ChatBubble from "@/components/chat_components/ChatBubble.vue";
import UserInput from "@/components/chat_components/UserInput.vue";
import { useChatStore } from "@/stores/chat";
import { setActivePinia } from "pinia";

const exampleMessages = [
    { message: "Hola 👋 ¿En qué puedo ayudarte hoy?", fromUser: false },
    {
        message:
            "Hola, estoy interesado en conocer más sobre sus servicios de marketing digital.",
        fromUser: true,
    },
    {
        message:
            "¡Excelente! Ofrecemos estrategias de marketing en redes sociales, SEO, publicidad pagada y creación de contenido. ¿Te interesa algún servicio en particular?",
        fromUser: false,
    },
    {
        message: "Me interesa principalmente la parte de redes sociales.",
        fromUser: true,
    },
];

test("renders mobile layout under 640px", async () => {
    window.innerWidth = 500;
    window.dispatchEvent(new Event("resize"));

    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const store = useChatStore();

    // adds messages
    exampleMessages.forEach((msg) => store.addMessage(msg));

    render(ChatView, {
        global: {
            stubs: { FontAwesomeIcon: true },
            components: { ChatComponent, ChatBubble, UserInput },
            plugins: [pinia],
        },
    });

    // get all bubbles then test for visibility
    const bubbles = screen.getAllByTestId("chat-bubble");
    for (const bubble of bubbles) {
        expect(bubble).toBeVisible();
    }

    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});

test("renders mobile layout under 1024px", async () => {
    window.innerWidth = 1000;
    window.dispatchEvent(new Event("resize"));

    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const store = useChatStore();

    // adds messages
    exampleMessages.forEach((msg) => store.addMessage(msg));

    render(ChatView, {
        global: {
            stubs: { FontAwesomeIcon: true },
            components: {
                ChatComponent,
                ChatBubble,
                UserInput,
            },
            plugins: [pinia],
        },
    });

    // get all bubbles then test for visibility
    const bubbles = screen.getAllByTestId("chat-bubble");
    for (const bubble of bubbles) {
        expect(bubble).toBeVisible();
    }
    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});

test("renders desktop layout with 1920px", async () => {
    window.innerWidth = 1920;
    window.dispatchEvent(new Event("resize"));

    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const store = useChatStore();

    // adds messages
    exampleMessages.forEach((msg) => store.addMessage(msg));

    render(ChatView, {
        global: {
            stubs: { FontAwesomeIcon: true },
            components: {
                ChatComponent,
                ChatBubble,
                UserInput,
            },
            plugins: [pinia],
        },
    });

    // get all bubbles then test for visibility
    const bubbles = screen.getAllByTestId("chat-bubble");
    for (const bubble of bubbles) {
        expect(bubble).toBeVisible();
    }
    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});

test("renders mobile layout with a 10 character input ", async () => {
    window.innerWidth = 500;
    window.dispatchEvent(new Event("resize"));

    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const message = `Rust is a prog`;
    const exampleMessages = [
        {
            message: message,
            fromUser: true,
        },
        {
            message: message,
            fromUser: false,
        },
    ];

    const store = useChatStore();
    store.clearChat();

    // adds messages
    exampleMessages.forEach((msg) => store.addMessage(msg));

    render(ChatView, {
        global: {
            stubs: { FontAwesomeIcon: true },
            components: {
                ChatComponent,
                ChatBubble,
                UserInput,
            },
            plugins: [pinia],
        },
    });

    // get all bubbles then test for visibility
    const bubbles = screen.getAllByTestId("chat-bubble");
    for (const bubble of bubbles) {
        expect(bubble).toBeVisible();
    }
    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});

test("renders mobile layout with a 1k+ character input ", async () => {
    window.innerWidth = 500;
    window.dispatchEvent(new Event("resize"));

    const pinia = createTestingPinia({ stubActions: false });
    setActivePinia(pinia);

    const message = `Rust is a programming language that stands out in the modern development ecosystem for its exceptional focus on performance, reliability, and safety. Designed with systems programming in mind, Rust achieves the elusive trifecta of speed, memory safety, and concurrency without compromising developer experience. One of its most lauded features is the ownership model, which ensures that memory management is deterministic and error-free at compile time, eliminating entire classes of bugs such as null pointer dereferencing and data races.

        Beyond technical rigor, Rust is also known for its empowering tooling. The built-in package manager and build system, Cargo, makes dependency management and project scaffolding a breeze. The compiler is famously friendly, offering helpful, human-readable error messages that guide developers toward better code. This makes Rust not only powerful but also approachable—even for developers new to low-level programming.

        Rust's ecosystem is vibrant and growing, supported by a passionate community that values inclusivity and transparency. Whether you're writing blazing-fast CLI tools, robust web servers with frameworks like Actix or Axum, or compiling to WebAssembly for frontend performance, Rust provides a compelling and safe environment to do so.

        In short, Rust is cool not just because of what it prevents, but because of what it enables: high-performance, low-overhead, and rock-solid software built with joy and confidence.`;

    const exampleMessages = [
        {
            message: message,
            fromUser: true,
        },
        {
            message: message,
            fromUser: false,
        },
    ];

    const store = useChatStore();
    store.clearChat();

    // adds 1k messages
    exampleMessages.forEach((msg) => store.addMessage(msg));

    render(ChatView, {
        global: {
            stubs: { FontAwesomeIcon: true },
            components: {
                ChatComponent,
                ChatBubble,
                UserInput,
            },
            plugins: [pinia],
        },
    });

    // get all bubbles then test for visibility
    const bubbles = screen.getAllByTestId("chat-bubble");
    for (const bubble of bubbles) {
        expect(bubble).toBeVisible();
    }
    expect(screen.getByTestId("navbar")).toBeVisible();
    expect(screen.getByTestId("user-input")).toBeVisible();
    expect(screen.getByTestId("button-send-message")).toBeVisible();
});