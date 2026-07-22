export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Pick = {
  id?: number;
  matchup: string;
  market: string;
  selection: string;
  sportsbook: string;
  american_odds: number;
  model_probability: number;
  edge_percent: number;
  expected_value_percent: number;
  confidence: number;
  units: number;
  status: string;
  explanation: string;
  starts_at: string;
};

export async function getFreePick(): Promise<Pick | null> {
  try {
    const response = await fetch(`${API_URL}/api/v1/picks/free`, {
      next: { revalidate: 300 }
    });
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}
