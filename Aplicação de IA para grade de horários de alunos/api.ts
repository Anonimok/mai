// Service layer to interact with the backend API

// Import types from the dedicated types file
import { Preferences, FileType, SessionResponse, UploadResponse, PreferencesResponse, ScheduleResponse, ErrorResponse } from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

async function handleResponse(response: Response): Promise<any> { // Return type can be more specific
    if (!response.ok) {
        let errorData: ErrorResponse;
        try {
            errorData = await response.json();
        } catch (e) {
            errorData = { error: `Erro ${response.status}: ${response.statusText}` };
        }
        throw new Error(errorData.error || `Erro ${response.status}: ${response.statusText}`);
    }
    return response.json();
}

export const apiService = {
    async createSession(): Promise<SessionResponse> {
        const response = await fetch(`${API_BASE_URL}/session`, {
            method: "POST",
        });
        return handleResponse(response);
    },

    async uploadFile(fileType: FileType, formData: FormData): Promise<UploadResponse> {
        // session_id should already be in formData
        const response = await fetch(`${API_BASE_URL}/upload/${fileType}`, {
            method: "POST",
            body: formData,
            // Headers are automatically set for FormData by fetch
        });
        return handleResponse(response);
    },

    async updatePreferences(sessionId: string, preferences: Preferences): Promise<PreferencesResponse> {
        const response = await fetch(`${API_BASE_URL}/schedule/preferences`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ session_id: sessionId, preferences: preferences }),
        });
        return handleResponse(response);
    },

    async generateSchedule(sessionId: string): Promise<ScheduleResponse> {
        const response = await fetch(`${API_BASE_URL}/schedule/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ session_id: sessionId }),
        });
        return handleResponse(response);
    },
};

