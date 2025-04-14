<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import ChatComponent from "@/components/ChatComponent.vue";
</script>

<template>
    <div class="flex flex-col h-full">
        <nav>
            <NavBar />
        </nav>
        <main class="flex-1 bg-background overflow-hidden">
            <ChatComponent />
        </main>
    </div>
</template>
