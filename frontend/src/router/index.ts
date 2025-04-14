import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ChatView from "@/views/ChatView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            redirect: "/chat-view",
            children: [
                {
                    path: "/chat-view",
                    name: "chat",
                    component: ChatView,
                },
            ],
        },
    ],
});

export default router
