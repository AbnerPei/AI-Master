## ADDED Requirements

### Requirement: Compile creator dossier into reusable skill assets
The system SHALL support compiling a sufficiently mature creator dossier into a reusable personal-understanding `skill` package.

#### Scenario: Build skill from mature creator dossier
- **WHEN** a creator dossier already contains stable identity, source index, evidence traceability, and distilled viewpoints
- **THEN** the system can generate a creator-specific `skill` package instead of requiring a separate manual rewrite

### Requirement: Skill output stays distinct from raw evidence
The system SHALL keep `skill` instructions separate from raw evidence files and source archives.

#### Scenario: Keep skill instructions clean
- **WHEN** a creator-specific `skill` is compiled
- **THEN** the generated `SKILL.md` contains trigger cues, operating guidance, boundaries, and distilled understanding rather than dumping raw metadata or full evidence blobs into the instructions

### Requirement: Skill output remains traceable to dossier evidence
The system SHALL preserve links from compiled `skill` assets back to the underlying creator dossier, source index, and key evidence records.

#### Scenario: Trace compiled skill to creator dossier
- **WHEN** a compiled `skill` presents a creator-specific method, pattern, or worldview
- **THEN** the related `skill` asset can reference the creator dossier or supporting source index where that understanding was derived

