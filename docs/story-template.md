# Finexio User Story Template

---

## [Title: Action-Oriented — What Gets Done]

**Synopsis:** [One sentence: what this delivers + why it matters.]

| Field | Value |
|-------|-------|
| **Epic / PRD** | [Link to parent] |
| **Priority** | `P0` · `P1` · `P2` |
| **Assignee** | [Assigned at sprint planning] |

---

### 1. User Story

> As a **[specific persona]**, I need to **[specific action]**, so that **[measurable outcome]**.

---

### 2. Why This Matters

- **Why we're building it:** [Business outcome — revenue, retention, ops efficiency, compliance]
- **Who asked for it:** [Name + context]
- **Cost of not building it:** [What keeps happening]

---

### 3. Current State & System Context

- **Current behavior:** [What the system does today]
- **Relevant code:** [Service name, repo, key files]
- **Key data entities:** [Tables, enums, schemas this story touches]
- **Gap this story closes:** [The specific limitation]

> ⚠️ If this section can't be populated, flag as blocker.

---

### 4. Acceptance Criteria

**Happy Path**
```
GIVEN  [precondition]
WHEN   [action]
THEN   [expected outcome]
AND    [additional outcome if needed]
```

**Edge Cases**
```
GIVEN  [edge condition]
WHEN   [action]
THEN   [expected behavior]
```

**Error / Failure States**
```
GIVEN  [failure condition]
WHEN   [action]
THEN   [what the user sees]
AND    [what the system logs]
```

**Business Rules**
- [Rule that must always hold]

---

### 5. Scope Boundaries

- [Excluded capability]
- [Excluded capability]

---

### 6. Modules — Include Only When Relevant

**Bulk & Scale**
- Batch size limit: [e.g., Max 200]
- Approval threshold: [e.g., >50 requires admin]
- Performance: [e.g., >100 runs async]

**Security & Compliance**
- Compliance constraints: [SOC2, PCI, Nacha]
- Sensitive data handling: [Encryption, masking, RBAC]

**Observability**
- Success metric: [e.g., "Support tickets drop ≥70% within 30 days"]
- Events / logging: [e.g., Emit `bulk_unenroll_success` with count]

---

### 7. Technical Notes *(optional)*

- Suggested approach: [Starting point]
- Data model impact: [New fields, migrations]
- API changes: [New/modified endpoints]
- Dependencies: [Other services, downstream consumers]

---

### 8. Definition of Done

- [ ] All acceptance criteria pass
- [ ] Unit tests for happy path + edge cases
- [ ] Integration test covers end-to-end flow
- [ ] Error states handled (user message + system log)
- [ ] Code reviewed and approved
- [ ] No regression in existing functionality
- [ ] Compliance check *(if security module applies)*
