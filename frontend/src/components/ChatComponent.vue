<!-- @ts-check -->
<script setup lang="ts">
import ChatBubble from "@/components/chat_components/ChatBubble.vue";
import UserInput from "@/components/chat_components/UserInput.vue";
import { useChatStore } from "@/stores/chat";
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { FwbSpinner } from "flowbite-vue";

const chat = useChatStore();
// this parses string to Date as pinia uses localStorage for persistence
// so when retrieving it gets plain text
chat.restoreTimestamps();
const isAtBottom = ref(true);
const loading = ref(false);
const scrollArea = ref<HTMLElement | null>(null);
const welcomeMessage = ref("");

/**
 * Does a stream-like animation
 */
async function welcomeTextStream() {
    welcomeMessage.value = "";
    const message = "Bienvenido~";
    for (let i = 0; i < message.length; i++) {
        welcomeMessage.value += message[i];
        await new Promise((resolve) => setTimeout(resolve, 50)); // typing speed
    }
}

// handles blur magic
function handleScroll() {
    if (!scrollArea.value) return;

    const { scrollTop, scrollHeight, clientHeight } = scrollArea.value;
    const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
    isAtBottom.value = distanceFromBottom < 20;
}

// handles message send by the user
function handleSendMessage(msg: string) {
    console.log("Message send by user:", msg);
    const chatMessage = { message: msg, fromUser: true };
    chat.addMessage(chatMessage);
    chat.addBotLoadingMessage();
    chat.assistantTrigger(msg);
}

// TODO: UPDATE THIS
// onMounted(() => {
//     chat.loadMessages();
// });

// const exampleMessages = [
//     { message: "Hola 👋 ¿En qué puedo ayudarte hoy?", fromUser: false },
//     { message: "Hola, quiero pedir unas papas fritas.", fromUser: true },
//     {
//         message:
//             "¡Perfecto! Tenemos papas fritas clásicas, con queso cheddar, o con tocino y salsa especial. Todas vienen en tamaño individual o para compartir. ¿Cuál prefieres?",
//         fromUser: false,
//     },
//     {
//         message: "Las clásicas están bien. ¿Cuánto cuestan las grandes?",
//         fromUser: true,
//     },
//     {
//         message:
//             "Las papas fritas clásicas grandes cuestan $3.200. También puedes agregarle una salsa extra por $500 si quieres darle un toque especial 🍟✨.",
//         fromUser: false,
//     },
//     {
//         message: "Perfecto, agrégame una por favor. ¿Cuánto demora?",
//         fromUser: true,
//     },
//     {
//         message:
//             "Tu pedido estará listo en aproximadamente 20 minutos. Puedes venir a retirarlo o pedir entrega a domicilio por $1.000 extra.",
//         fromUser: false,
//     },
//     { message: "Lo retiro yo. Gracias!", fromUser: true },
//     {
//         message: "¡De nada! Te esperamos. Que tengas un buen día 😊",
//         fromUser: false,
//     },
// ];

const messages = computed(() => chat.messages);

// gets the dummy element at the bottom
const bottomEl = ref<HTMLElement | null>(null);
// TODO: MAYBE CONSIDER NOT SCROLLING ON NEW MESSAGES TBD
// on new messages scrolls to the bottom
watch(messages.value, async () => {
    await nextTick(); // wait for DOM to update
    bottomEl.value?.scrollIntoView({ behavior: "smooth" });
});

// watches changes directly in the messages
watch(messages, async () => {
    if (messages.value.length == 0) {
        welcomeTextStream();
    }
});

onMounted(() => {
    welcomeTextStream();

    // on mounted moves the scroll to the bottom
    loading.value = true;

    setTimeout(() => {
        loading.value = false;
    }, 500);

    setTimeout(() => {
        bottomEl.value?.scrollIntoView({ behavior: "smooth" });
    }, 1000);
});
</script>

<template>
    <!-- chat container -->
    <div class="flex h-full flex-col bg-white rounded-t-4xl p-5">
        <!-- messages -->
        
        
        <div
            
            class="flex flex-col flex-1 overflow-y-auto min-h-0"
            ref="scrollArea"
            @scroll="handleScroll"
        >
            <!-- blur magic -->
            <!-- blur magic banned hasta nuevo aviso, tiene dramas con el auto focus -->
            <!-- <div
                v-if="isAtBottom"
                class="sticky top-0 z-10 min-h-20 bg-gradient-to-b from-white to-transparent pointer-events-none"
            ></div> -->
            <div v-if="messages.length == 0" class="flex flex-1 text-center justify-center align-items-middle transition-all">
                <div class="flex pt-20 text-middle">
                    <p class="text-4xl bg-gradient-to-tr from-background to-sky-300 bg-clip-text text-transparent font-semibold ">
                        {{welcomeMessage}}
                    </p>
                </div>
            </div>

            <div v-else class="flex flex-1">
                <div v-if="!loading" class="flex flex-col flex-1">
                    <ChatBubble
                        v-for="msg in messages"
                        :key="msg.id"
                        :id="msg.id"
                        :message="msg.message"
                        :from-user="msg.fromUser"
                        :loading="msg.loading"
                        :bottomEl="bottomEl"
                        :timeStamp="msg.timestamp"
                    />
                </div>
                <div v-else class="flex flex-1 justify-center items-center">
                    <fwb-spinner size="12" />
                </div>
            </div>

            

            <!-- dummy element to scroll into view -->
            <div ref="bottomEl" class="h-px"></div>
        </div>

        <!-- the writing part -->
        <div class="flex min-h-16 justify-center bg-amber-300">
            <UserInput @send="handleSendMessage" />
        </div>
    </div>
</template>

<style scoped></style>
