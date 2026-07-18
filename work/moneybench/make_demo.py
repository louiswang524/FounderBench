from __future__ import annotations

import html
import json
from pathlib import Path

from moneybench.cli import run


ROOT = Path(__file__).resolve().parents[2]
OUTPUTS = ROOT / "outputs"


AGENTS = [
    {
        "name": "Astra Vale",
        "role": "CEO / Allocator",
        "initials": "AV",
        "focus": "Capital allocation, market selection, risk control",
        "actions": ["do_nothing"],
        "accent": "#2563a8",
    },
    {
        "name": "Mira Signal",
        "role": "Market Research",
        "initials": "MS",
        "focus": "Demand signals, competition, willingness to pay",
        "actions": ["research_market"],
        "accent": "#1f8a5b",
    },
    {
        "name": "Kade Forge",
        "role": "Product Builder",
        "initials": "KF",
        "focus": "Offer quality, product packaging, iteration",
        "actions": ["build_offer", "improve_offer"],
        "accent": "#b87913",
    },
    {
        "name": "Nia Reach",
        "role": "Growth / Sales",
        "initials": "NR",
        "focus": "Awareness, campaign quality, acquisition",
        "actions": ["run_campaign"],
        "accent": "#8d4fb3",
    },
    {
        "name": "Owen Care",
        "role": "Customer Ops",
        "initials": "OC",
        "focus": "Support load, retention, reputation",
        "actions": ["support_customers", "hire_agent"],
        "accent": "#bc3e36",
    },
]


def agent_for_action(action_type: str) -> dict:
    for agent in AGENTS:
        if action_type in agent["actions"]:
            return agent
    return AGENTS[0]


def describe_action(action: dict) -> str:
    target = action.get("market_id") or action.get("offer_id") or "company"
    budget = action.get("budget") or 0
    price = action.get("price")
    detail = f"{action['type']} on {target}"
    if budget:
        detail += f" with {budget:.0f} AC"
    if price:
        detail += f" at {price:.0f} AC"
    return detail


def make_deliberation(event: dict) -> dict:
    actions = event["actions"]
    result = event["result"]
    primary = actions[0] if actions else {"type": "do_nothing"}
    owner = agent_for_action(primary["type"])
    action_text = "; ".join(describe_action(action) for action in actions) or "hold position"
    profit = result["profit"]
    risk = result["risk_penalty"]
    traction = result["new_customers"]

    if primary["type"] == "research_market":
        ceo = "We need cleaner information before spending real budget. Research the strongest unresolved market signal."
    elif primary["type"] == "build_offer":
        ceo = "The signals are good enough to create a focused offer. Fund quality now so future campaigns have something worth selling."
    elif primary["type"] == "improve_offer":
        ceo = "The product is close, but quality is the bottleneck. Improve the offer before pushing more demand into it."
    elif primary["type"] == "run_campaign":
        ceo = "The offer is ready enough to test demand. Run a controlled campaign and watch conversion before scaling."
    elif primary["type"] == "support_customers":
        ceo = "Revenue only matters if customers stay. Invest in support to protect reputation and recurring value."
    elif primary["type"] == "hire_agent":
        ceo = "Capacity is becoming a constraint. Add an agent worker so support load does not damage reputation."
    else:
        ceo = "No action has a strong enough expected return this week. Preserve capital and wait."

    discussion = [
        {
            "agent": "Astra Vale",
            "stance": "proposal",
            "text": ceo,
        },
        {
            "agent": "Mira Signal",
            "stance": "market read",
            "text": "Prioritize demand minus competition, not just high ticket size. Expensive markets can still be bad if buyers are hard to reach.",
        },
        {
            "agent": "Kade Forge",
            "stance": "product read",
            "text": "Underfunded builds create weak conversion. If we build, fund quality enough to avoid a low-trust offer.",
        },
        {
            "agent": "Nia Reach",
            "stance": "growth read",
            "text": "Campaign spend should follow offer readiness. Awareness is useful only when quality and price fit are credible.",
        },
        {
            "agent": "Owen Care",
            "stance": "ops read",
            "text": "Support and reputation compound. If customers arrive, protect retention before chasing another market.",
        },
    ]

    if risk > 0:
        discussion.append(
            {
                "agent": "Astra Vale",
                "stance": "risk objection",
                "text": f"This plan carries {risk:.0f} risk penalty. Keep the action bounded and do not repeat it without evidence.",
            }
        )
    if traction > 0:
        discussion.append(
            {
                "agent": "Nia Reach",
                "stance": "traction update",
                "text": f"The market responded with {traction} new customer{'s' if traction != 1 else ''}. Continue scaling only if support remains healthy.",
            }
        )

    if profit >= 0:
        decision_reason = "approved because expected compounding value exceeds weekly operating cost"
    else:
        decision_reason = "approved as an investment week; near-term loss is acceptable if it increases future conversion or signal quality"

    return {
        "owner": owner["name"],
        "owner_role": owner["role"],
        "objective": action_text,
        "discussion": discussion,
        "decision": {
            "status": "approved",
            "reason": decision_reason,
            "assigned_to": owner["name"],
            "expected_effect": "increase information quality, offer strength, market awareness, or retention",
        },
    }


def main() -> None:
    result = run("heuristic", seed=7, weeks=20, trace=True)
    for event in result["events"]:
        event["deliberation"] = make_deliberation(event)
    trace_path = OUTPUTS / "moneybench-demo-trace.json"
    html_path = OUTPUTS / "moneybench-demo.html"
    trace_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    events_json = json.dumps(result["events"])
    summary_json = json.dumps(result["summary"])
    agents_json = json.dumps(AGENTS)
    html_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MoneyBench Demo</title>
  <style>
    :root {{
      --bg: #f6f7f2;
      --panel: #ffffff;
      --ink: #1d252c;
      --muted: #62717d;
      --line: #d9e0e5;
      --green: #1f8a5b;
      --blue: #2563a8;
      --gold: #b87913;
      --red: #bc3e36;
      --violet: #8d4fb3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }}
    main {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 22px;
      display: grid;
      gap: 16px;
    }}
    h1 {{ margin: 0; font-size: 30px; letter-spacing: 0; }}
    h2 {{ margin: 0 0 10px; font-size: 13px; text-transform: uppercase; color: var(--muted); letter-spacing: .06em; }}
    .top {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }}
    .summary, .viewer, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .agent-strip {{
      display: grid;
      grid-template-columns: repeat(5, minmax(160px, 1fr));
      gap: 10px;
    }}
    .agent {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      display: grid;
      grid-template-columns: 46px 1fr;
      gap: 10px;
      align-items: center;
      min-height: 104px;
      transition: border-color .2s, box-shadow .2s, transform .2s;
    }}
    .agent.active {{
      border-color: var(--green);
      box-shadow: 0 0 0 3px rgba(31, 138, 91, .12);
      transform: translateY(-1px);
    }}
    .avatar {{
      width: 46px;
      height: 46px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: white;
      font-weight: 800;
      font-size: 14px;
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.36);
      background:
        radial-gradient(circle at 30% 22%, rgba(255,255,255,.45), transparent 26px),
        var(--accent);
    }}
    .agent strong {{ display: block; font-size: 14px; }}
    .agent span {{ display: block; color: var(--muted); font-size: 12px; line-height: 1.35; margin-top: 2px; }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(5, minmax(130px, 1fr));
      gap: 1px;
      overflow: hidden;
    }}
    .metric {{
      padding: 14px;
      background: var(--panel);
    }}
    .metric span {{ display: block; color: var(--muted); font-size: 13px; margin-bottom: 6px; }}
    .metric strong {{ font-size: 23px; }}
    .viewer {{
      padding: 16px;
      display: grid;
      gap: 16px;
    }}
    .controls {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}
    button {{
      height: 38px;
      border-radius: 8px;
      border: 1px solid var(--line);
      background: var(--panel);
      padding: 0 12px;
      cursor: pointer;
      color: var(--ink);
      font: inherit;
    }}
    button.primary {{ background: var(--green); border-color: var(--green); color: white; }}
    input[type="range"] {{ flex: 1 1 260px; accent-color: var(--green); }}
    .grid {{
      display: grid;
      grid-template-columns: .9fr 1.1fr;
      gap: 14px;
    }}
    .decision-grid {{
      display: grid;
      grid-template-columns: .75fr 1.25fr;
      gap: 14px;
    }}
    .card {{ padding: 14px; min-height: 180px; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin: 7px 0; color: var(--muted); line-height: 1.4; }}
    code {{
      background: #edf2ef;
      padding: 2px 5px;
      border-radius: 6px;
      color: #274d3a;
    }}
    .profit {{ color: var(--green); }}
    .loss {{ color: var(--red); }}
    .timeline {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(34px, 1fr));
      gap: 4px;
    }}
    .process {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }}
    .stage {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfb;
      min-height: 74px;
    }}
    .stage.active {{ border-color: var(--green); box-shadow: 0 0 0 3px rgba(31, 138, 91, .10); }}
    .stage b {{ display: block; margin-bottom: 4px; }}
    .stage span {{ color: var(--muted); font-size: 12px; line-height: 1.35; }}
    .tick {{
      height: 12px;
      border-radius: 99px;
      background: #dfe5e0;
    }}
    .tick.active {{ background: var(--green); }}
    pre {{
      white-space: pre-wrap;
      word-break: break-word;
      margin: 0;
      font-size: 12px;
      color: var(--muted);
    }}
    .decision {{
      border-left: 4px solid var(--green);
      padding-left: 12px;
      display: grid;
      gap: 8px;
    }}
    .decision strong {{ font-size: 18px; }}
    .decision span {{ color: var(--muted); line-height: 1.4; }}
    .chat {{
      display: grid;
      gap: 10px;
    }}
    .message {{
      display: grid;
      grid-template-columns: 42px 1fr;
      gap: 10px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfb;
    }}
    .message-avatar {{
      width: 42px;
      height: 42px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      color: white;
      font-size: 13px;
      font-weight: 800;
      background:
        radial-gradient(circle at 28% 22%, rgba(255,255,255,.42), transparent 24px),
        var(--accent);
    }}
    .message b {{ display: block; font-size: 14px; }}
    .message small {{ display: block; color: var(--muted); margin: 2px 0 6px; text-transform: uppercase; letter-spacing: .05em; font-size: 11px; }}
    .message p {{ margin: 0; color: #344550; line-height: 1.42; }}
    @media (max-width: 800px) {{
      .summary {{ grid-template-columns: repeat(2, 1fr); }}
      .grid, .decision-grid {{ grid-template-columns: 1fr; }}
      .agent-strip {{ grid-template-columns: 1fr; }}
      .process {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>
<main>
  <div class="top">
    <div>
      <h1>MoneyBench Process Demo</h1>
      <p>Heuristic agent, seed 7, 20 simulated weeks. Step through observe -> action -> outcome.</p>
    </div>
    <button class="primary" id="play">Play</button>
  </div>

  <section class="summary" id="summary"></section>

  <section class="agent-strip" id="agents"></section>

  <section class="viewer">
    <div class="controls">
      <button id="prev">Prev</button>
      <input id="week" type="range" min="0" max="0" value="0">
      <button id="next">Next</button>
      <strong id="label"></strong>
    </div>
    <div class="timeline" id="timeline"></div>
    <div class="process" id="process"></div>
    <div class="decision-grid">
      <section class="card">
        <h2>CEO Decision Patch</h2>
        <div class="decision" id="decision"></div>
      </section>
      <section class="card">
        <h2>Agent Debate</h2>
        <div class="chat" id="discussion"></div>
      </section>
    </div>
    <div class="grid">
      <section class="card">
        <h2>Company State Before Action</h2>
        <ul id="state"></ul>
      </section>
      <section class="card">
        <h2>Agent Actions</h2>
        <ul id="actions"></ul>
      </section>
      <section class="card">
        <h2>Simulator Result</h2>
        <ul id="result"></ul>
      </section>
      <section class="card">
        <h2>Raw Event</h2>
        <pre id="raw"></pre>
      </section>
    </div>
  </section>
</main>
<script>
const events = {events_json};
const summary = {summary_json};
const agents = {agents_json};
let index = 0;
let timer = null;

function money(v) {{
  return Math.round(v).toLocaleString() + " AC";
}}

function renderSummary() {{
  document.getElementById("summary").innerHTML = [
    ["Final Score", Math.round(summary.score).toLocaleString()],
    ["Final Cash", money(summary.cash)],
    ["Customers", summary.customers],
    ["Reputation", summary.reputation],
    ["Bankrupt", summary.bankrupt ? "yes" : "no"],
  ].map(([k, v]) => `<div class="metric"><span>${{k}}</span><strong>${{v}}</strong></div>`).join("");
}}

function activeActionTypes(event) {{
  return new Set(event.actions.map(action => action.type));
}}

function renderAgents(event) {{
  const activeTypes = activeActionTypes(event);
  document.getElementById("agents").innerHTML = agents.map(agent => {{
    const active = agent.actions.some(action => activeTypes.has(action));
    return `
      <article class="agent ${{active ? "active" : ""}}" style="--accent:${{agent.accent}}">
        <div class="avatar">${{agent.initials}}</div>
        <div>
          <strong>${{agent.name}}</strong>
          <span>${{agent.role}}</span>
          <span>${{agent.focus}}</span>
        </div>
      </article>
    `;
  }}).join("");
}}

function renderProcess(event) {{
  const types = activeActionTypes(event);
  const stages = [
    ["Sense", "Research market signals", types.has("research_market")],
    ["Build", "Create or improve the offer", types.has("build_offer") || types.has("improve_offer")],
    ["Sell", "Run acquisition campaigns", types.has("run_campaign")],
    ["Operate", "Support, hire, or hold", types.has("support_customers") || types.has("hire_agent") || types.has("do_nothing")],
  ];
  document.getElementById("process").innerHTML = stages.map(([title, text, active]) => `
    <div class="stage ${{active ? "active" : ""}}">
      <b>${{title}}</b>
      <span>${{text}}</span>
    </div>
  `).join("");
}}

function agentByName(name) {{
  return agents.find(agent => agent.name === name) || agents[0];
}}

function renderDeliberation(event) {{
  const d = event.deliberation;
  document.getElementById("decision").innerHTML = `
    <strong>${{htmlEscape(d.objective)}}</strong>
    <span>Status: <code>${{htmlEscape(d.decision.status)}}</code></span>
    <span>Assigned to: <code>${{htmlEscape(d.decision.assigned_to)}}</code> (${{htmlEscape(d.owner_role)}})</span>
    <span>Reason: ${{htmlEscape(d.decision.reason)}}</span>
    <span>Expected effect: ${{htmlEscape(d.decision.expected_effect)}}</span>
  `;
  document.getElementById("discussion").innerHTML = d.discussion.map(msg => {{
    const agent = agentByName(msg.agent);
    return `
      <article class="message" style="--accent:${{agent.accent}}">
        <div class="message-avatar">${{agent.initials}}</div>
        <div>
          <b>${{htmlEscape(msg.agent)}}</b>
          <small>${{htmlEscape(msg.stance)}}</small>
          <p>${{htmlEscape(msg.text)}}</p>
        </div>
      </article>
    `;
  }}).join("");
}}

function render() {{
  const event = events[index];
  document.getElementById("week").max = events.length - 1;
  document.getElementById("week").value = index;
  document.getElementById("label").textContent = `Week ${{event.week}} / ${{events.length}}`;
  document.getElementById("timeline").innerHTML = events.map((_, i) => `<div class="tick ${{i === index ? "active" : ""}}"></div>`).join("");
  renderAgents(event);
  renderProcess(event);
  renderDeliberation(event);
  document.getElementById("state").innerHTML = [
    `Cash before action: <strong>${{money(event.cash)}}</strong>`,
    `Actions submitted: <strong>${{event.actions.length}}</strong>`,
  ].map(x => `<li>${{x}}</li>`).join("");
  document.getElementById("actions").innerHTML = event.actions.map(action => {{
    const target = action.market_id || action.offer_id || "company";
    const budget = action.budget ? `, budget ${{money(action.budget)}}` : "";
    const price = action.price ? `, price ${{money(action.price)}}` : "";
    return `<li><code>${{action.type}}</code> on <code>${{target}}</code>${{budget}}${{price}}</li>`;
  }}).join("");
  const cls = event.result.profit >= 0 ? "profit" : "loss";
  document.getElementById("result").innerHTML = [
    `Revenue: <strong>${{money(event.result.revenue)}}</strong>`,
    `Cost: <strong>${{money(event.result.cost)}}</strong>`,
    `Profit: <strong class="${{cls}}">${{money(event.result.profit)}}</strong>`,
    `New customers: <strong>${{event.result.new_customers}}</strong>`,
    `Churned customers: <strong>${{event.result.churned_customers}}</strong>`,
    `Risk penalty: <strong>${{event.result.risk_penalty}}</strong>`,
    ...event.result.notes.map(n => htmlEscape(n))
  ].map(x => `<li>${{x}}</li>`).join("");
  document.getElementById("raw").textContent = JSON.stringify(event, null, 2);
}}

function htmlEscape(s) {{
  return String(s).replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}}[c]));
}}

function stop() {{
  if (timer) clearInterval(timer);
  timer = null;
  document.getElementById("play").textContent = "Play";
}}

document.getElementById("prev").onclick = () => {{ stop(); index = Math.max(0, index - 1); render(); }};
document.getElementById("next").onclick = () => {{ stop(); index = Math.min(events.length - 1, index + 1); render(); }};
document.getElementById("week").oninput = e => {{ stop(); index = Number(e.target.value); render(); }};
document.getElementById("play").onclick = () => {{
  if (timer) return stop();
  document.getElementById("play").textContent = "Pause";
  timer = setInterval(() => {{
    index = index >= events.length - 1 ? 0 : index + 1;
    render();
  }}, 1100);
}};

renderSummary();
render();
</script>
</body>
</html>
""",
        encoding="utf-8",
    )
    print(f"Wrote {html_path}")
    print(f"Wrote {trace_path}")


if __name__ == "__main__":
    main()
