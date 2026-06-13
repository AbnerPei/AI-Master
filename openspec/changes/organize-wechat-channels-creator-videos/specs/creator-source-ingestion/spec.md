## ADDED Requirements

### Requirement: Multi-source ingestion
The system SHALL support attaching multiple source types to the same creator identity record, including but not limited to `视频号`, `公众号`, and `书籍`.

#### Scenario: Attach wechat channels source
- **WHEN** a user starts from a `视频号` seed
- **THEN** the ingested source is recorded as one source entry under the target creator identity rather than as a standalone platform-only artifact

#### Scenario: Attach additional source type later
- **WHEN** a user later provides a `公众号` article or book reference for the same person
- **THEN** the new material is attached to the existing creator identity record as an additional source entry

### Requirement: Prefer local video capture for video sources
The system SHALL attempt to preserve a local media copy for video-based source entries whenever a downloadable video file is obtainable during ingestion.

#### Scenario: Save local video copy
- **WHEN** a `视频号` source entry can be downloaded as a local video file during ingestion
- **THEN** the source entry records the local video path or artifact reference alongside the original source link

#### Scenario: Degrade gracefully when download is unavailable
- **WHEN** a `视频号` source entry cannot be downloaded as a local video file
- **THEN** the system still records the source entry with available metadata and marks that the media artifact is missing or download failed

### Requirement: Source entries remain attributable
The system SHALL preserve source-native metadata for each ingested source entry so later distillation can cite where an idea or claim came from.

#### Scenario: Preserve source-native keys
- **WHEN** a source entry is ingested
- **THEN** the record keeps the original link, identifier, title or description, and capture metadata that were available from that source

### Requirement: Published time is mandatory for video evidence
The system SHALL record a clear published-time field set for each video-based source entry, including the best available publish time value, the precision of that value, and the evidence source from which it was derived.

#### Scenario: Record exact publish timestamp
- **WHEN** the source provides an exact video publish timestamp
- **THEN** the source entry stores that timestamp as the authoritative published time and marks its precision as exact

#### Scenario: Record non-exact publish date
- **WHEN** the source provides only a date or an imprecise publish-time representation
- **THEN** the source entry stores the available value and marks its precision accordingly instead of silently treating it as an exact timestamp
