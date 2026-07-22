"use client";

import { FormEvent, useState } from "react";
import { API_URL } from "@/lib/api";

export default function Login() {
  const [message, setMessage] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const response = await fetch(`${API_URL}/api/v1/auth/login`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({email: form.get("email"), password: form.get("password")})
    });
    const data = await response.json();
    if (!response.ok) return setMessage(data.detail ?? "Login failed");
    localStorage.setItem("edgeboard_token", data.access_token);
    window.location.href = "/dashboard";
  }

  return (
    <main className="container">
      <form className="card form" onSubmit={submit}>
        <div className="eyebrow">Welcome back</div>
        <h2>Log in to EdgeBoard</h2>
        <label>Email<input className="input" name="email" type="email" required /></label>
        <label>Password<input className="input" name="password" type="password" required /></label>
        <button className="button primary" style={{width:"100%"}}>Log in</button>
        {message && <p className="muted">{message}</p>}
      </form>
    </main>
  );
}
