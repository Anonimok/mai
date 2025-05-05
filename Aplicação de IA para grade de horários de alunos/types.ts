// Define shared types here

export type FileType = 'catalog' | 'history' | 'curriculum';

export interface Preferences {
  min_creditos: number;
  max_creditos: number;
  // Add other preference types here
}

export interface Horario {
  dia_semana: string;
  horario_inicio: string;
  horario_fim: string;
  inicio_min: number;
  fim_min: number;
}

export interface Disciplina {
  codigo: string;
  nome: string;
  turma: string;
  horarios: Horario[];
}

export interface Schedule {
  disciplinas: Disciplina[];
  creditos: number;
  // score?: number; // Optional score
}

export interface UploadStatus {
  catalog: boolean;
  history: boolean;
  curriculum: boolean;
}

// API Response Types (adjust as needed)
export interface SessionResponse {
    session_id: string;
    message?: string;
}

export interface UploadResponse {
    message: string;
    file_path?: string;
}

export interface PreferencesResponse {
    message: string;
}

export interface ScheduleResponse {
    solutions: Schedule[]; // Use the Schedule type defined above
    message?: string;
}

export interface ErrorResponse {
    error: string;
}

