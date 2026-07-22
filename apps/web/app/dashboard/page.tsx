"use client";

import { useEffect, useState } from "react";
import { API_URL, Pick } from "@/lib/api";
import { PickCard } from "@/components/PickCard";

export default function Dashboard() {
  const [picks, setPicks] = useState<Pick[]>([]);
  const [message, setMessage] = useState("Loading your board...");

  useEffect(() => {
    const token = localStorage.getItem("edgeboard_token");
    if (!token) {
      window.location.href = "/login";
      return;
    }
    fetch(`${API_URL}/api/v1/picks`, {
      headers: {Authorization: `Bearer ${token}`}
    })
      .then(async (response) => {
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail ?? "Unable to load board");
        setPicks(data);
        setMessage("");
      })
      .catch((error) => setMessage(error.message));
  }, []);

  return (
    <main className="section container">
      <div className="eyebrow">Subscriber dashboard</div>
      <h1 style={{fontSize:"58px", textAlign:"left", marginLeft:0}}>Today&apos;s official card</h1>
      <p className="section-lead">Every play is filtered for edge, expected value, confidence, and risk.</p>
      {message && <div className="card">{message}</div>}
      <div className="grid">
        {picks.map((pick, index) => <PickCard key={pick.id ?? index} pick={pick} />)}
      </div>
    </main>
  );
}
