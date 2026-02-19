# Sample Questions — Agentic Investment Team

Use these to test each architecture and agent. Questions are grouped by which agent/team/workflow they target.

---

## Route Team (Single-agent dispatch)

These should route to exactly one specialist.

1. **What's AAPL's current P/E ratio?** → Financial Analyst
2. **Is NVDA in a bullish or bearish trend right now?** → Technical Analyst
3. **What's the latest news on Tesla?** → Market Analyst
4. **What's the risk profile of a $2M MSFT position?** → Risk Officer
5. **What past investment memos do we have on file?** → Knowledge Agent
6. **What does our research say about the AI semiconductor sector?** → Knowledge Agent
7. **Write an investment memo for Apple.** → Memo Writer
8. **How should we allocate $5M across our top picks?** → Committee Chair
9. **What did we decide about NVIDIA last time?** → Knowledge Agent
10. **What's Amazon's free cash flow and debt situation?** → Financial Analyst

---

## Coordinate Team (Chair orchestrates dynamically)

Open-ended investment questions that benefit from multi-analyst discussion.

11. **Should we invest $2M in NVIDIA?**
12. **Evaluate Microsoft for a potential $1.5M position.**
13. **Is now a good time to add semiconductor exposure to our portfolio?**
14. **We're considering a $1M position in Meta — what does the committee think?**
15. **Should we increase our tech allocation or diversify into healthcare?**

---

## Broadcast Team (Parallel independent evaluation)

High-stakes decisions where you want independent analyst opinions.

16. **Full committee review: evaluate Tesla for a $2M allocation.**
17. **All analysts: assess Google for our portfolio. BUY or PASS?**
18. **Committee vote: should we invest $1.5M in Amazon?**
19. **Independent evaluation: is Apple a buy at current levels for a $2M position?**

---

## Task Team (Autonomous decomposition)

Complex multi-step tasks that require planning and parallel work.

20. **Deploy $10M across the top 5 AI stocks, no single position over 30%.**
21. **Build a diversified portfolio: $3M in tech, $2M in healthcare, $1M in energy.**
22. **Rebalance our portfolio to reduce tech concentration below 40%.**
23. **Compare NVDA, AMD, and AVGO — which is the best semiconductor bet and at what allocation?**
24. **Create a defensive portfolio of $5M that minimizes drawdown risk.**

---

## Investment Workflow (Deterministic 5-step pipeline)

Full investment reviews that should follow the fixed process.

25. **Run full investment review on NVIDIA.**
26. **Process Apple through the complete investment pipeline.**
27. **Standard review: evaluate Google for purchase.**
28. **Run the full evaluation process on Microsoft for a $2M position.**

---

## Stress Tests (Edge cases and mandate compliance)

Questions that test risk limits, mandate rules, and institutional learning.

29. **Should we put $5M into Tesla?** (Exceeds max single position for high-beta stock)
30. **We already have 35% in tech. Can we add a $2M NVDA position?** (Tests sector cap)
31. **Analyze a $500K position in a penny stock trading at $3.** (Prohibited by mandate)
32. **What's the maximum we can invest in any single stock?** (Tests Layer 1 knowledge)
33. **If we hold both NVDA and AMD, what's our correlation risk?** (Tests correlation limit)
34. **We have $500K cash remaining. Should we deploy it or maintain the reserve?** (Tests 5% cash reserve rule)

---

## Knowledge & Memory Tests

Questions that test the three-layer knowledge system and institutional learning.

35. **What does our NVIDIA research profile say about their competitive moat?** (Layer 2 — RAG)
36. **Pull up the Tesla memo — what was the committee's decision?** (Layer 3 — FileTools)
37. **What are our fund's position size limits?** (Layer 1 — should be in every agent's context)
38. **What sector research do we have available?** (Layer 2 — RAG discovery)
39. **Summarize all past investment decisions.** (Layer 3 — multi-memo retrieval)
40. **What is our investment mandate?** (Layer 1 — system prompt context)
