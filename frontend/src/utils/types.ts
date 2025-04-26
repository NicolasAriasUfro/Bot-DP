export interface ChatMessage {
    id: string;
    message: string;
    fromUser: boolean;
    timestamp: Date;
    loading: boolean;
}

export interface AssistantResponse {
    message: string;
}
