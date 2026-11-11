# Design rationale (catalog)

Short map from [SPEC.md](SPEC.md) demo behaviour to published work. **SPEC wins** on product scope; this file exists for hackathon catalog reviewers who want citations without re-reading the full spec.

We only cite claims already stated in SPEC or implied by the 90-second demo outline there—nothing extra.

---

## Demo claims → research

| Demo / product claim (from SPEC) | Research anchor | How Oracle implements it (SPEC) |
| --- | --- | --- |
| People stay optimistic from the **inside view** (“this time I’ll finish on time”). | **Planning fallacy** — Buehler, Griffin, & Ross (1994) | Forecasts must not stop at pep talk; odds use **similar past attempts** (git/calendar history) with reasons shown. |
| Connecting **this** plan to **similar past attempts** matters more than vague memory of being late. | Same; SPEC frames this alongside **outside view** / reference class | With fewer than three similar cases: **no invented percentage**; still track and settle. Demo: “Ship search this week” odds from similar weeks or “not enough history.” |
| **Outside view**: adjust this week using what comparable plans actually produced. | Outside view / reference-class forecasting (see Lovallo & Kahneman, 2003) | Busy calendar → shipping odds drop after comparable history; mirror compares guess vs proof. |
| A worse forecast is **not** automatic nagging. | **JITAI** — Nahum-Shani et al. (2016) | Nudge only if slipping **and** **receptive**; otherwise **provide nothing**. Demo step 3: subtract or silence. |
| **Subtract** is a product hypothesis, not a validated intervention from these papers. | — | JITAI motivates *when* to speak, not *that* cutting scope always works (SPEC table). |

**Demo-safe one-liners** (SPEC, not study results on Oracle):

- Planning-fallacy work suggests optimism persists unless past misses are tied to *this* plan — Oracle starts from named similar attempts.
- JITAI-style design treats silence as valid when you’re not receptive — a dropping forecast does not always mean an interruption.

**Explicit non-claims** (catalog copy must not imply):

- A few personal weeks are as solid as large public-project reference classes.
- JITAI proves “subtract” is the best action.
- Brier / calibration claims from one or two settled commitments.

---

## References (short)

1. **Buehler, R., Griffin, D., & Ross, M. (1994).** Exploring the “planning fallacy”: Why people underestimate their task completion times. *Journal of Personality and Social Psychology*, *67*(3), 366–381. [https://doi.org/10.1037/0022-3514.67.3.366](https://doi.org/10.1037/0022-3514.67.3.366)

2. **Nahum-Shani, I., Smith, S. N., Spring, B. J., Collins, L. M., Witkiewitz, K., Tewari, A., & Murphy, S. A. (2016).** Just-in-time adaptive interventions (JITAIs) in mobile health: Key components and design principles for ongoing health behavior support. *Annals of Behavioral Medicine*. [https://doi.org/10.1007/s12160-016-9830-8](https://doi.org/10.1007/s12160-016-9830-8)

3. **Lovallo, D., & Kahneman, D. (2003).** Delusions of success: How optimism undermines executives’ decisions. *Harvard Business Review*, *81*(7), 56–63, 137. (Outside view and reference-class forecasting in organizational planning—the vocabulary SPEC uses for “similar past attempts.”)

---

## Maintenance

Behaviour changes grounded in research: update this file when [SPEC.md](SPEC.md) § “Research vs what we built” or the demo script changes (SPEC working agreement).
