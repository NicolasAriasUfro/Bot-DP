<script setup lang="ts">
import { computed } from "vue";
import { FwbSpinner } from "flowbite-vue";

const props = defineProps<{
    message: string;
    fromUser?: boolean;
    loading: boolean;
}>();

const bubbleClasses = computed(() =>
    props.fromUser
        ? "bg-secondary max-w-76 sm:max-w-md text-text-dark rounded-b-2xl rounded-tl-xl self-end"
        : "bg-white max-w-xs sm:max-w-md text-black rounded-b-2xl rounded-tr-xl self-start"
);
</script>

<template>
    <div
        data-testid="chat-bubble"
        class="flex items-start gap-2 m-2"
        :class="{ 'self-end': fromUser, 'self-start': !fromUser }"
    >
        <div v-if="!fromUser" class="pt-2 pl-2">
            <!-- TODO: CHANGE CUESTIONABLE LOOKING ICON -->
            <font-awesome-icon icon="fa-solid fa-robot" size="lg" />
        </div>
        <div
            class="flex p-3 m-2 min-w-15 text-sm sm:text-base outline-1"
            :class="bubbleClasses"
        >
            <div v-if="!loading">{{ message }}</div>
            <div v-else class="flex justify-center items-center">
                <fwb-spinner size="6" />
            </div>
        </div>
    </div>
</template>
