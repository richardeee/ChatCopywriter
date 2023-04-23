export type ChatResponse = {
    answer: ChatMessage;
    thoughts: string | null;
    data_points: string[];
    error?: string;
};

export type ChatMessage = {
    role: string;
    text: string;
    time?: string;
}