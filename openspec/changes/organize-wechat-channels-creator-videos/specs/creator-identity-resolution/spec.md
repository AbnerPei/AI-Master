## ADDED Requirements

### Requirement: Person-first seed resolution
The system SHALL accept a creator seed from a content link, creator page, known handle, or manually provided name, and SHALL resolve that seed into a person-first creator identity record before any source-specific ingestion continues.

#### Scenario: Resolve creator from single content link
- **WHEN** a user provides a single `视频号` video link as the initial seed
- **THEN** the system creates or updates a creator identity record that captures the visible creator name, the seed source, and any source-native identifiers available at resolution time

#### Scenario: Continue with partial identity
- **WHEN** the system cannot obtain a stable cross-platform identifier from the first seed
- **THEN** the system still creates a provisional creator identity record that can accept more sources later without discarding the original seed context

### Requirement: Alias-aware identity merging
The system SHALL allow one creator identity record to preserve aliases, platform handles, and naming variants so that future sources can be merged into the same person record.

#### Scenario: Merge new source with name variant
- **WHEN** a later source refers to the same person using a different platform handle or visible name
- **THEN** the system preserves the new alias on the existing creator identity record instead of creating a parallel creator record by default

