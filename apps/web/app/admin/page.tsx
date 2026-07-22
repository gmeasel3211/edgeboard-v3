"use client";

import { useState } from "react";
import { API_URL, authHeaders } from "@/lib/api";

const actions = [
  ["Full refresh", "/api/v1/admin/refresh/full"],
  ["MLB data", "/api/v1/admin/refresh/mlb"],
  ["Odds + model", "/api/v1/admin/refresh/odds"],
  ["Weather", "/api/v1/admin/refresh/weather"],
  ["Rebuild card", "/api/v1/admin/rebuild-card"],
];

export default function AdminPage() {
  const [output, setOutput] = useState("Select an operation.");

  async function run(path: string) {
    setOutput("Running...");
    const response = await fetch(`${API_URL}${path}`, {
      method: "POST",
      headers: authHeaders(),
    });
    const data = await response.json();
    setOutput(JSON.stringify(data, null, 2));
  }

  return (
    <main className="section container">
      <div className="eyebrow">Administrator</div>
      <h1 style={{fontSize:"58px", textAlign:"left", marginLeft:0}}>Data control center</h1>
      <div className="actions" style={{justifyContent:"flex-start"}}>
        {actions.map(([label, path]) => (
          <button className="button primary" onClick={() => run(path)} key={path}>{label}</button>
        ))}
      </div>
      <pre className="card" style={{marginTop:"24px", whiteSpace:"pre-wrap", overflow:"auto"}}>{output}</pre>
    </main>
  );
}
