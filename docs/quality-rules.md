# PRD & Story Quality Rules

Derived from real Finexio failures. Enforce on every output.

---

## The Rules

### Rule 1: Transform, Don't Polish
If input is a request form (Section 1/2/3 format, intake template), **transform** it into PRD structure. The intake form is input, not output.

### Rule 2: PRD ≠ Stories
PRD = what and why (one page). Stories = individual buildable units with ACs. Never combine them. PRDs reference stories. Stories reference the PRD.

### Rule 3: Find the Real Persona
Don't accept the persona from the intake form at face value. Who has the workflow pain? If intake says "As a customer" but the real pain is operational (SE/AM teams), fix it.

### Rule 4: Given/When/Then Only
Bullet-point requirements labeled "Acceptance Criteria" are not acceptance criteria. Every AC needs happy path, edge cases, and error states. An engineer writes tests directly from ACs.

### Rule 5: System Reality Check Is Mandatory
Can't populate current implementation, what changes, what doesn't? Flag it as a blocker. A PRD without system context is a request, not a requirement.

### Rule 6: One Feature Per Story
Multiple features bundled = scope confusion. Different personas, different systems, or different implementation paths = separate stories.

### Rule 7: Explicit Exclusions
Every PRD must state what is NOT in scope. "This PRD does NOT include..." If you can't identify exclusions, generate likely candidates and flag for confirmation.

### Rule 8: Open Questions Must Block, Not Float
Unanswered questions need three things: (1) What's the question, (2) Who answers it, (3) What changes in the PRD if answered differently. If the question is reversible, decide now and move.

### Rule 9: Output Replaces Input
Never paste the original request at the bottom "for reference." If the output is complete, the original is redundant. If not, iterate.

### Rule 10: Quantified Success Metrics
"Operational efficiency" is not a metric. Every PRD needs at least two measurable outcomes with baseline, target, method, and timeframe.

### Rule 11: SCQ Every Problem Statement
Use Situation → Complication → Question format. If you can't write the complication in one sentence, the scope is too broad. If you can't phrase the question as "How do we...?", you haven't found the real problem yet.

### Rule 12: Tag Decisions as Reversible or Irreversible
Reversible decisions (can change after launch) should be made immediately by the PM. Irreversible decisions (data model changes, API contracts, compliance implications) need stakeholder input before proceeding. Don't let reversible decisions slow you down.

### Rule 13: Match Solution Complexity to the Problem
Don't propose AI when "lock the field" works. Lead with the simplest solution that solves 80% of the problem, not the most impressive solution. Overengineering signals to reviewers that you don't understand the real business need.

### Rule 14: Verify Team/Role Assignments with Actual Team Members  
Don't guess who owns what. Wrong team assignments signal that the PRD author doesn't understand the org structure. Research current ownership or explicitly flag as "VERIFY: Is this Operations or SE?" when uncertain.

### Rule 15: Distinguish Known Facts from Assumptions
Mark assumptions clearly as "VERIFY:" Don't present guesses as facts. Research findings should be cited with sources. When you're making logical inferences, say so. Reviewers need to know what's confirmed vs. what needs validation.

### Rule 16: Read the Source Request Literally First  
Expand scope only with stakeholder confirmation. If the ClickUp ticket says "PairSoft supplier changes," don't automatically scope it to "all partners" without checking. The initial request defines baseline scope. Additions need explicit buy-in.

### Rule 17: Flag Secondary Sources
Flag if input source is not the domain owner. Secondary sources may describe symptoms, not root causes. If request comes from someone other than the team experiencing the operational pain, trigger conversational intake mode to validate the problem framing.

### Rule 18: SME Response Timeouts
If Problem Brief gets no SME response in 48 hours, escalate or proceed with assumptions clearly marked as UNVALIDATED. Don't let SME delays block delivery indefinitely, but make the risk visible in the final PRD.

### Rule 19: Research Completeness Gate
Gate for Step 2 research = can fill all 6 Brief fields with confidence. If not, mark gaps as UNKNOWN for SME to fill. Don't guess at scope, solution direction, or key assumptions — better to surface unknowns explicitly than make wrong assumptions.

---

## Common Failure Patterns

| Failure | What Goes Wrong | Prevention |
|---------|-----------------|------------|
| Wrong persona | "As a customer" when pain is internal ops | Identify who has the workflow pain |
| Vague title | "Update supplier bulk updater" | Action-oriented, outcome-focused title |
| Bullet-point ACs | "Should work for all payment types" | Given/When/Then only |
| No system context | Engineer reverse-engineers before coding | Populate Current State from code/docs |
| No scope boundaries | Nobody defined what's NOT included | Explicit exclusions required |
| Missing "why" | Developer doesn't know if corner can be cut | Business Rationale preserved |
| Multi-feature bundling | Three features in one ticket | Split into separate stories |
| Original request pasted | Two conflicting versions | Output replaces input |
| Missing bulk/scale thinking | Works for 5 items, crashes at 500 | Include batch limits, async thresholds |
| Compliance afterthought | Security issue caught in release review | Address SOC2/PCI/Nacha up front |
| Novel-length problem statement | Reader gives up before reaching requirements | SCQ format — 4 lines max |
| Over-deliberation | Reversible decision treated as irreversible | Tag and triage decisions |
| Partner scope ambiguity | Built for direct buyer, partner needs differ | Flag Context as Partner up front |

---

## Bad vs Good Examples

### Bad: Request Form Disguised as PRD

```
Title: ER ON HOLD: Restore "Unknown" Enrollment Delay Alert Case Type

Section 1: Core Information
Request Type: Enhancement
Product Area: Customer Portal
...
[Original request pasted at bottom]
```

Problems: Not a PRD structure, wrong persona, bullet-point ACs, no system context, no scope boundaries.

### Good: Actual PRD

```
# PRD: Non-vCard Enrollment Delay Alerts in Customer Portal

## 1. Problem Statement
- **Situation:** SE team manages supplier enrollment campaigns through the portal, including delay alerts.
- **Complication:** Non-vCard delay alert case types were removed, forcing SE/AM teams into manual spreadsheet tracking.
- **Question:** How do we restore SE team's ability to work non-vCard enrollment delay cases through the standard portal workflow?
- **Cost of inaction:** ~15 manual requests/week, missed enrollment campaigns, fragmented workflows.

## 2. Business Rationale
- **Strategic alignment:** Supplier enablement throughput directly impacts payment volume
- **Revenue impact:** Enrollment delays = suppliers not enrolled = revenue left on table
- **Requesting stakeholder:** Theresa B. / Supplier Enablement

[...continues with full template sections...]
```

### Bad: Vague Story

```
Title: Update supplier bulk updater
Description: As a user, I want to update supplier enrollment in bulk so that it's easier.
AC: Should work for all payment types. Should have confirmation screen.
```

Problems: No persona, no system context, no Given/When/Then, no scope boundaries.

### Good: Sprint-Ready Story

```
# Bulk Unenroll Card-by-Mail Suppliers

**Story:** As an AP operations manager, I need to bulk unenroll card-by-mail suppliers, so that I don't submit 15+ manual requests per week.

**Current State:** BulkUpdateController in supplier-enrollment-service handles ACH and vCard but not card-by-mail. No unenroll endpoint exists.

**AC:**
GIVEN selected suppliers include card-by-mail
WHEN bulk unenroll submitted
THEN card-by-mail enrollment status updated to inactive
AND confirmation email sent to each supplier

GIVEN supplier has pending payments
WHEN unenroll attempted
THEN system blocks with error "Cannot unenroll supplier with pending payments"

**Scope Boundaries:**
- Does NOT include export functionality
- Does NOT include automated notifications beyond confirmation
```
