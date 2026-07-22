import Link from "next/link";

const plans = [
  { name: "Free", price: "$0", features: ["Daily free preview", "Public model record", "Weekly newsletter"] },
  { name: "Pro", price: "$29", features: ["Full MLB card", "Edge and EV metrics", "Recommended units", "Performance center"] },
  { name: "Elite", price: "$59", features: ["Everything in Pro", "Advanced game breakdowns", "Priority alerts", "Early feature access"] }
];

export default function Pricing() {
  return (
    <main className="section container">
      <div className="eyebrow">Memberships</div>
      <h1 style={{fontSize: "58px", textAlign: "left", marginLeft: 0}}>Simple plans. Serious tools.</h1>
      <div className="grid grid-3 pricing">
        {plans.map((plan) => (
          <div className="card" key={plan.name}>
            <div className="eyebrow">{plan.name}</div>
            <div className="price">{plan.price}<span className="muted" style={{fontSize: "16px"}}>/month</span></div>
            {plan.features.map((feature) => <div className="feature" key={feature}>{feature}</div>)}
            <Link className="button primary" style={{width:"100%", marginTop:"20px"}} href="/register">Choose {plan.name}</Link>
          </div>
        ))}
      </div>
    </main>
  );
}
