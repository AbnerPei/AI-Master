## ADDED Requirements

### Requirement: Distilled creator profile
The system SHALL maintain a creator distillation profile that summarizes who the person is, what topics they repeatedly cover, and what stable viewpoints or methods emerge across sources.

#### Scenario: Record recurring themes
- **WHEN** multiple source entries for the same creator repeatedly discuss similar ideas
- **THEN** the distillation profile captures those ideas as recurring themes instead of leaving them only as disconnected source notes

#### Scenario: Record methods or frameworks
- **WHEN** the creator repeatedly presents a named method, workflow, or decision pattern across sources
- **THEN** the distillation profile captures that method as part of the creator's reusable viewpoint or framework

### Requirement: Distillation remains time-traceable
The system SHALL allow distilled judgments about a creator to trace back to source entries with clear publish-time information, so changes in viewpoint can be examined in chronological order.

#### Scenario: Trace insight to published video
- **WHEN** the distillation profile cites a claim or method drawn from a video source
- **THEN** the profile can reference the underlying source entry together with its recorded publish time and time precision

### Requirement: Incremental distillation updates
The system SHALL support refining the creator distillation profile as new sources are added without requiring the profile to be regenerated from scratch every time.

#### Scenario: Refine profile with later source
- **WHEN** a new `公众号` article or book excerpt adds nuance or contradiction to an existing creator summary
- **THEN** the distillation profile is updated while preserving the link between new conclusions and the newly added evidence
