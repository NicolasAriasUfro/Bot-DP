<script setup lang="ts">
import FunctionButton from "@/components/FunctionButton.vue";
import { useChatStore } from "@/stores/chat";

const chatStore = useChatStore();

function newsFunction() {
    const message = "¿Cuáles son las últimas noticias?";
    const userMessage = "¿Cual son las noticias en la actualidad?";
    callStore(message, userMessage);
}

function weatherFunction() {
    const message = "Dame el clima en Temuco";
    const userMessage = "¿Me puedes decir el clima en Temuco?";
    callStore(message, userMessage);
}

function ufFunction() {
    const message = "¿Cuál es el valor de la uf?";
    const userMessage = "¿Cual es el valor actual de la UF?";
    callStore(message, userMessage);
}

function dolarFunction() {
    const message = "¿Cuál es el valor del dolar?";
    const userMessage = "¿Cual es el valor actual del Dolar?";
    callStore(message, userMessage);
}

function callStore(message: string, userMessage: string) {
    const chatMessage = { message: userMessage, fromUser: true };
    chatStore.addMessage(chatMessage);
    chatStore.addBotLoadingMessage();
    chatStore.assistantTrigger(message);
}
</script>

<template>
    <div>
        <transition name="fade">
            <div class="flex flex-col m-10">
                <FunctionButton
                    :icon="'🌡️'"
                    :label="'El Clima'"
                    :onButtonClick="weatherFunction"
                />

                <FunctionButton
                    :icon="'📰'"
                    :label="'Las Noticias'"
                    :onButtonClick="newsFunction"
                />

                <FunctionButton
                    :icon="'💵'"
                    :label="'La Uf'"
                    :onButtonClick="ufFunction"
                />

                <FunctionButton
                    :icon="'📈'"
                    :label="'El Dolar'"
                    :onButtonClick="dolarFunction"
                />
            </div>
        </transition>
    </div>
</template>
