<script setup lang="ts">
import { FwbButton, FwbInput } from "flowbite-vue";
import { ref } from "vue";

const userInput = ref("");

const emit = defineEmits<{
    (e: "send", message: string): void;
}>();

function onSend() {
    if (!userInput.value.trim()) return;
    emit("send", userInput.value.trim());
    userInput.value = "";
}
</script>

<template>
    <form
        @submit.prevent="onSend"
        class="flex flex-1 justify-center items-center bg-white"
    >
        <input
            v-model="userInput"
            type="text"
            class="flex-1 rounded-full border px-4 py-2 focus:border-background focus:ring-0"
            placeholder="Escribe un mensaje.."
        />
        <button
            type="submit"
            :disabled="!userInput.trim()"
            class="ml-2 px-3 py-2 bg-background text-white rounded-full hover:bg-blue-600 outline-1 outline-text-dark disabled:opacity-50 disabled:cursor-not-allowed"
        >
            <font-awesome-icon icon="fa-solid fa-paper-plane" />
        </button>
    </form>
</template>
