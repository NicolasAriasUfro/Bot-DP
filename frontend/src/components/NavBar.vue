<script lang="ts" setup>
import { useChatStore } from "@/stores/chat";
import { FwbSpinner } from "flowbite-vue";
import { computed } from "vue";

const chatStore = useChatStore();

function NuevoChatBtn() {
    chatStore.clearChat();
} 

const messages = computed(() => chatStore.messages);

const lastMessageStatus = computed(() => {
    if (messages.value.length > 0) {
        return messages.value[messages.value.length - 1].loading
    }
    return false
})

</script>

<template>
    <nav
        data-testid="navbar"
        class="flex bg-background p-4 min-h-[64px] h-20 justify-center items-center"
    >
        <button
            :disabled="lastMessageStatus"
            type="button"
            @click="NuevoChatBtn"
            class="text-text-dark bg-gradient-to-tr from-stone-50 to-sky-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-lg text-sm px-4 py-2.5 text-center shadow-lg"
        >
            <!-- TODO: do magic here -->
            <div v-if="true" class="flex justify-between">
                <div class="mr-2">
                    <font-awesome-icon
                        icon="fa-solid fa-pen-to-square"
                        size="lg"
                    />
                </div>
                <p>Iniciar Nuevo Chat</p>
            </div>
            <div v-else><fwb-spinner /></div>
        </button>
    </nav>
</template>

<style lang="scss" scoped></style>
