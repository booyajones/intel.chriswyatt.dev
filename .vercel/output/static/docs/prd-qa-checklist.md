# PRD QA Checklist

Run this checklist against EVERY PRD before delivering to Chris. No exceptions.

## Branding (Non-Negotiable)
- [ ] Finexio logo in document header (from `powerpoint/finexio-deck-builder/assets/logo_primary_color.png`)
- [ ] Navy accent line under header (#043886)
- [ ] "Finexio | Confidential" in footer
- [ ] Table headers use navy background (#043886) with white text
- [ ] Alternate row shading on tables (#EDF2FA)
- [ ] Font: Calibri throughout
- [ ] Priority labels color-coded: P0 red, P1 amber, P2 blue
- [ ] Document is .docx format (Word)

## Structure (Per Template)
- [ ] Metadata table present with all required fields
- [ ] Section 1: Problem Statement uses SCQ format (Situation, Complication, Question)
- [ ] Section 2: Business Rationale includes strategic alignment, revenue impact, operational impact, requesting stakeholder
- [ ] Section 3: User Story in "As a [persona], I need [capability], so that [outcome]" format
- [ ] Section 4: Functional Requirements split into P0/P1/P2 with testable behaviors
- [ ] Section 5: System Reality Check includes current implementation, what changes, what doesn't change
- [ ] Section 6: Constraints includes compliance, dependencies, explicit exclusions ("This PRD does NOT include..."), risk
- [ ] Section 7: Success Metrics table with baseline, target, method, timeframe
- [ ] Section 8: Decisions (with rationale/who/date) + Open Questions (with reversible tag)

## Content Quality
- [ ] No em-dashes (use -- instead)
- [ ] No emojis
- [ ] No AI filler ("Great question!", "I'd be happy to help!")
- [ ] Stakeholder quotes preserved where available
- [ ] Research summary included (what was found, where)
- [ ] Scope exclusions are specific, not generic
- [ ] Success metrics are quantified with baselines
- [ ] Decisions tagged with who decided and when

## Research
- [ ] ClickUp ticket fully parsed (description, custom fields, attachments, watchers)
- [ ] Confluence searched for related docs
- [ ] Research findings cited in System Reality Check and Research Summary sections
- [ ] Gaps flagged as Open Questions (not silently ignored)

## Delivery
- [ ] Word doc generated and attached (not just markdown)
- [ ] File sent to Slack with brief summary
- [ ] Summary highlights any open questions or gaps
