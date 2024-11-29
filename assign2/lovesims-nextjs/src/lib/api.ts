const API_BASE_URL = 'http://127.0.0.1:5000'

export async function startDates(data: {
  mode: string;
  agents: string[];
  dateContext?: string;
  dateDuration: number;
}) {
  const response = await fetch(`${API_BASE_URL}/start_dates`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

export function createEventSource() {
  return new EventSource(`${API_BASE_URL}/stream`);
}

export async function runDates() {
  const response = await fetch(`${API_BASE_URL}/run_dates`, {
    method: 'POST',
  });
  return response.json();
}

export async function resetGame() {
  const response = await fetch(`${API_BASE_URL}/reset`, {
    method: 'POST',
  });
  return response.json();
}

export type EvaluationType = 'self-reflection' | 'transcript-based' | 'profiles-based' | 'all';

export interface EvaluationResult {
  type: EvaluationType;
  analysis: string;
  compatibilityScore?: number;
  satisfactionScore?: number;
  lengthFeedback?: string;
  attributeImportance?: Record<string, number>;
}

export async function runEvaluation(data: {
  type: EvaluationType;
  mode: string;
  agents: string[];
  transcript: any[];
}) {
  const response = await fetch(`${API_BASE_URL}/evaluate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return response.json() as Promise<EvaluationResult[]>;
}
