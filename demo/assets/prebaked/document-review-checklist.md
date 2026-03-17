# Document Review Checklist -- L&LL Master Services Agreement

**Generated:** 2026-01-16
**Reviewer:** Agentic Contract Analyzer v1
**Document:** Master Services Agreement between L&LL LLC and Six Feet Up, Inc.
**Effective Date:** January 15, 2026

---

## Summary

The MSA is broadly standard for a consulting engagement but contains
**5 significant issues** and **3 moderate concerns** that should be
addressed before execution.

| Risk Level | Count | Action |
|---|---|---|
| CRITICAL | 2 | Must renegotiate before signing |
| HIGH | 3 | Strongly recommend renegotiation |
| MEDIUM | 3 | Recommend clarification |
| LOW | 2 | Acceptable, monitor |

---

## CRITICAL Issues

### 1. Overbroad IP Assignment (Section 4.1-4.2)

**Risk:** CRITICAL
**Clause:** Section 4.1 and 4.2 -- Assignment of Work Product

**Finding:** The IP assignment clause extends far beyond standard
work-for-hire provisions:

- Assigns ALL work product "regardless of whether such work product was
  created during working hours, using Consultant's own equipment, or
  **developed prior to the Effective Date**."
- The trigger is merely that "Consultant had knowledge of Client's
  business or potential business needs" -- an extraordinarily low bar.
- Section 4.2 irrevocably assigns **Pre-Existing IP** incorporated into
  any Deliverable, directly contradicting the definition in Section 1.4.
- Moral rights waiver is included without limitation.

**Impact:** Six Feet Up could lose ownership of its own pre-existing
frameworks, libraries, and tools if any are used in delivering services.
This effectively transfers Consultant's core business assets to Client.

**Recommendation:**
- Replace with standard work-for-hire language that assigns only
  Deliverables created specifically under an SOW.
- Add a "Consultant Tools" carve-out: Consultant retains ownership of
  pre-existing IP and grants Client a perpetual, non-exclusive license
  to use it as embedded in Deliverables.
- Remove the "knowledge of Client's business" trigger entirely.
- Remove or narrow the moral rights waiver.

---

### 2. Unreasonable Non-Compete (Section 6.1)

**Risk:** CRITICAL
**Clause:** Section 6.1 -- Non-Competition

**Finding:** The non-compete is almost certainly unenforceable and is
unreasonably punitive:

- **Duration:** 24 months post-termination (industry standard is 6-12
  months, if any).
- **Geographic scope:** Worldwide, with no limitation.
- **Scope of restricted activity:** Includes any business that
  "Client has discussed pursuing" -- not limited to activities actually
  undertaken.
- **Breadth:** Covers "tabletop gaming content," "streaming or digital
  media related to role-playing games" -- this would prevent Consultant
  from working with a huge segment of the tech and gaming industry.

**Impact:** If enforced, Six Feet Up could not serve any client in the
gaming, LARP, or adjacent entertainment space for two years globally.
This is disproportionate for a consulting engagement.

**Recommendation:**
- Reduce duration to 6 months maximum, or remove entirely.
- Limit geographic scope to Client's actual markets.
- Restrict to direct competitors only, not broadly-defined industries.
- Remove "discussed pursuing" language -- limit to actual business
  activities.
- Consider replacing with a narrower non-solicitation of Client's
  customers.

---

## HIGH Issues

### 3. One-Sided Indemnification (Section 8)

**Risk:** HIGH
**Clause:** Section 8.1 vs 8.2 -- Indemnification

**Finding:** The indemnification obligations are dramatically
asymmetric:

- **Consultant's obligation (8.1):** Indemnifies Client for six broad
  categories including "any use by Client of the Deliverables, whether
  or not such use was foreseeable by Consultant." This makes Consultant
  liable for Client's own misuse of deliverables.
- **Client's obligation (8.2):** Only indemnifies against claims arising
  from Client's *unauthorized* use of Deliverables -- a nearly
  impossible standard to trigger.

**Impact:** Consultant bears virtually all risk, including for outcomes
outside its control.

**Recommendation:**
- Make indemnification mutual and symmetric.
- Remove clause 8.1(f) entirely (liability for Client's use of
  Deliverables).
- Add mutual carve-outs for gross negligence and willful misconduct.
- Add a duty-to-mitigate clause.

---

### 4. Missing Data Protection Provisions

**Risk:** HIGH
**Clause:** Not present

**Finding:** The Agreement contains **no data protection or privacy
provisions** despite the engagement involving:

- Migration of Client's web properties (likely containing user data)
- Access to Client's database dumps
- Potential handling of customer PII from larpsy.gold marketplace

**Missing provisions:**
- No Data Processing Agreement (DPA)
- No GDPR/CCPA compliance requirements
- No data breach notification obligations
- No data residency or sovereignty requirements
- No data retention and deletion policies
- No sub-processor restrictions

**Impact:** Both parties are exposed to regulatory risk. If L&LL has EU
customers (likely for a global online marketplace), GDPR applies and a
DPA is legally required.

**Recommendation:**
- Add a Data Protection section or attach a DPA as an exhibit.
- Specify data handling, retention, and deletion requirements.
- Include data breach notification timelines (72 hours for GDPR).
- Define sub-processor approval process.
- Add CCPA/state privacy law compliance if applicable.

---

### 5. Auto-Renewal Buried in General Provisions (Section 12.11)

**Risk:** HIGH
**Clause:** Section 12.11 -- Renewal

**Finding:** An auto-renewal clause is buried in "General Provisions"
(Section 12) rather than in "Term and Termination" (Section 10) where
a reader would expect to find it:

- Agreement auto-renews for successive 12-month periods.
- Non-renewal requires 60 days' written notice before term end.
- Combined with Section 6.1 (non-compete), this creates a trap: if
  Consultant misses the 60-day window, the Agreement renews for another
  year, and the 24-month non-compete clock resets.
- All fee schedules from active SOWs carry forward unchanged.

**Impact:** Risk of unintended commitment. The placement appears
designed to be overlooked during review.

**Recommendation:**
- Move renewal terms to Section 10 (Term and Termination).
- Reduce auto-renewal period to month-to-month after initial term.
- Add a conspicuous notice requirement before auto-renewal takes effect.
- Decouple non-compete from renewal (non-compete should run from
  original termination, not renewal termination).

---

## MEDIUM Issues

### 6. Limitation of Liability Favors Client (Section 9)

**Risk:** MEDIUM
**Clause:** Section 9

**Finding:** Liability limitations apply asymmetrically:

- Section 9.1 limits Client's liability for indirect/consequential
  damages but no reciprocal limitation for Consultant.
- Section 9.2 caps Client's total liability at 12 months of fees paid
  but does not cap Consultant's liability.
- Combined with the broad indemnification in Section 8, Consultant has
  uncapped exposure.

**Recommendation:**
- Make liability cap mutual.
- Add a reciprocal exclusion of consequential damages.
- Cap both parties' total liability at fees paid in the preceding 12
  months.

---

### 7. Unilateral Termination for Convenience (Section 10.3)

**Risk:** MEDIUM
**Clause:** Section 10.3

**Finding:** Only Client has termination-for-convenience rights.
Consultant can only terminate for cause. The 15-day notice period is
also short for a consulting engagement where Consultant may have
allocated staff.

**Recommendation:**
- Grant mutual termination-for-convenience rights.
- Extend notice period to 30 days.
- Add a kill-fee or minimum payment for early termination covering
  Consultant's costs of resource reallocation.

---

### 8. Dispute Resolution Venue (Section 12.3)

**Risk:** MEDIUM
**Clause:** Section 12.3

**Finding:** Binding arbitration in Wilmington, Delaware. While
Delaware is a neutral jurisdiction, arbitration costs can be
significant and there is no provision for:

- Fee allocation (loser pays vs. each party bears own costs)
- Selection of arbitrator(s)
- Scope of discoverable materials

**Recommendation:**
- Specify arbitrator selection process.
- Add fee-shifting provision (prevailing party recovers reasonable
  costs).
- Consider mediation as a mandatory first step before arbitration.

---

## LOW / Acceptable

### 9. Standard Confidentiality (Section 5)

**Risk:** LOW

**Finding:** Confidentiality provisions are standard and reasonable.
Five-year survival period is within normal range. Standard exceptions
are included.

**Status:** Acceptable as drafted.

---

### 10. Insurance Requirements (Section 11)

**Risk:** LOW

**Finding:** Insurance requirements are reasonable for this type of
engagement. $1M CGL and $2M E&O are standard.

**Status:** Acceptable as drafted.

---

## Adversarial Analysis -- Red Flags

An adversarial review (simulating opposing counsel's likely intent)
identified the following patterns:

1. **The IP Trap:** Sections 4.1 + 4.2 are drafted to capture
   Consultant's pre-existing IP. The "knowledge of Client's business"
   trigger in 4.1 means that once Consultant learns about L&LL's
   business (which happens by reading this Agreement), nearly all
   subsequent work could be claimed.

2. **The Lock-In Loop:** Section 12.11 (auto-renewal) + Section 6.1
   (non-compete) create a compounding lock: missing the renewal window
   extends the non-compete by another year, and the non-compete prevents
   working with competitors even after the relationship ends.

3. **The Indemnity Sink:** Section 8.1(f) makes Consultant liable for
   Client's own use of Deliverables. Combined with the unlimited
   liability (no cap for Consultant in Section 9), this creates
   open-ended financial exposure.

4. **Missing Privacy as Leverage:** The absence of data protection
   provisions means Client can later claim Consultant failed to meet
   "industry standards" for data handling -- useful leverage in a
   dispute.

---

## Recommended Action

**Do not sign as drafted.** Negotiate the following changes at minimum:

1. Rewrite Section 4 with a Consultant Tools carve-out and standard
   work-for-hire assignment limited to SOW Deliverables.
2. Remove or drastically narrow Section 6.1 (non-compete).
3. Make Section 8 (indemnification) mutual and symmetric.
4. Add a Data Protection exhibit / DPA.
5. Move Section 12.11 (auto-renewal) into Section 10 and add
   conspicuous notice requirements.
