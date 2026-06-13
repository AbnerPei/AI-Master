## ADDED Requirements

### Requirement: Evidence and conclusion separation
The system SHALL store raw or minimally processed source evidence separately from distilled conclusions about the creator.

#### Scenario: Keep source evidence traceable
- **WHEN** the system stores a source excerpt, raw metadata file, or capture artifact
- **THEN** that evidence remains linked to the creator identity and to its originating source entry without being rewritten as a conclusion

#### Scenario: Keep conclusion traceable to evidence
- **WHEN** a distilled insight about the creator is recorded
- **THEN** the insight references one or more source entries or evidence items that support it

### Requirement: Video evidence completeness
The system SHALL track the completeness of video-based evidence, including whether a local media file exists and whether the publish time is exact, date-only, estimated, or unknown.

#### Scenario: Track full video evidence
- **WHEN** a video source entry has a local media file and an exact publish timestamp
- **THEN** the evidence index marks that video evidence as locally preserved and time-confirmed

#### Scenario: Track partial video evidence
- **WHEN** a video source entry is missing a local media file or only has an imprecise publish time
- **THEN** the evidence index records the missing artifact or lower time precision explicitly instead of treating the evidence as complete

### Requirement: Layer-aware placement
The system SHALL place creator evidence artifacts in locations that preserve the existing knowledge-base layer boundaries between `Clippings/` and `raw/`.

#### Scenario: Preserve clipping artifacts
- **WHEN** ingestion produces raw page exports, screenshots, raw `JSON`, or other acquisition byproducts
- **THEN** those artifacts remain in `Clippings/` or a clearly scoped descendant path of that layer

#### Scenario: Preserve normalized evidence records
- **WHEN** the system writes normalized evidence records or creator-linked source indexes
- **THEN** those records are stored in `raw/` as knowledge-source artifacts instead of being mixed into temporary clipping outputs

#### Scenario: Preserve local media artifacts
- **WHEN** ingestion produces a local video file for a source entry
- **THEN** the local media artifact is stored in a stable evidence location and linked from the normalized evidence record
