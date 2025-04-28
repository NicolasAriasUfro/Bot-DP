<script setup lang="ts">
const props = defineProps<{
    icon: string;
    label: string;
    onButtonClick: () => void;
}>();
</script>

<template>
    <button
        @click="props.onButtonClick"
        class="flex flex-row px-4 py-5 my-2 text-lg text-text-dark bg-gradient-to-tr from-stone-50 to-sky-200 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-cyan-300 dark:focus:ring-cyan-800 font-medium rounded-lg text-center shadow-lg transition-all duration-1000 ease-in-out"
    >
        <div class="flex flex-1 justify-center">
            <p>{{ props.icon }}</p>
        </div>
        <div class="flex flex-3">
            <p>{{ props.label }}</p>
        </div>
    </button>
</template>
