<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue";
import { FwbSpinner } from "flowbite-vue";

const props = defineProps<{
    id: string;
    message: string;
    fromUser?: boolean;
    loading: boolean;
    timeStamp: Date;
    bottomEl: HTMLElement | null; // cucha: questionable html element as prop but it works
}>();

const displayedText = ref("");

// types message in a 'stream-like' manner
const typeMessage = async (message: string) => {
    for (let i = 0; i < message.length; i++) {
        displayedText.value += props.message[i];

        // updates the scroll
        await nextTick();
        props.bottomEl?.scrollIntoView({ behavior: "smooth" });

        await new Promise((resolve) => setTimeout(resolve, 10)); // typing speed
    }
};

const bubbleClasses = computed(() =>
    props.fromUser
        ? "bg-secondary max-w-76 sm:max-w-md text-text-dark rounded-b-2xl rounded-tl-xl self-end"
        : "bg-white max-w-xs sm:max-w-md text-black rounded-b-2xl rounded-tr-xl self-start"
);

watch(
    // watches loading status
    // if the value goes from false -> true then is new
    // and does the stream
    () => props.loading,
    (newLoadingState, oldLoadingState) => {
        if (!newLoadingState && oldLoadingState) {
            typeMessage(props.message);
        } else {
            displayedText.value = props.message;
        }
    },
    { immediate: true }
);
</script>

<template>
    <div
        data-testid="chat-bubble"
        class="flex items-start gap-2 m-2 transition-all duration-700 transition-normal"
        :class="{ 'self-end': fromUser, 'self-start': !fromUser }"
    >
        <div v-if="!fromUser" class="pt-2 pl-2">
            <!-- TODO: CHANGE CUESTIONABLE LOOKING ICON -->
            <font-awesome-icon icon="fa-solid fa-robot" size="lg" />
        </div>
        <div class="flex flex-col">
            <div
            class="flex px-3 pt-3 pb-1 m-2 min-w-15 text-sm sm:text-base outline-1"
            :class="bubbleClasses"
            >
                <div v-if="!loading" class="whitespace-normal break-normal wrap-anywhere">
                    {{ displayedText  }} 
                    <div class="text-end text-xs mt-1">
                        {{ props.timeStamp.toLocaleTimeString() }}
                    </div>
                </div>
                <div v-else class="flex pb-2 justify-center items-center">
                    <fwb-spinner size="6" />
                </div>
            </div>
        </div>
    </div>
</template>
