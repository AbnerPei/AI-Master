## ADDED Requirements

### Requirement: Enumerate creator content from a single seed
The system SHALL support starting from a single `视频号` content `url` and producing a creator-scoped content list for that same person, even if the first seed only exposes one video directly.

#### Scenario: Expand from one seed video
- **WHEN** a user provides one `视频号` video link for a creator
- **THEN** the system records the seed video and attempts to discover the same creator's broader content list instead of stopping at the single video

### Requirement: Mixed acquisition strategy for creator enumeration
The system SHALL support more than one enumeration strategy for creator content discovery, with public-page or public-response parsing preferred first and desktop-client automation allowed as a fallback.

#### Scenario: Use public discovery path first
- **WHEN** a creator content list can be inferred from public page data, public response data, or stable link relations
- **THEN** the system records that the creator catalog was discovered through a public acquisition path

#### Scenario: Fall back to desktop automation
- **WHEN** the public discovery path cannot produce a stable creator content list
- **THEN** the system may use `Mac WeChat` automation or another local-client enumeration path and records that fallback strategy explicitly

### Requirement: Creator catalog entries are normalized
The system SHALL normalize enumerated creator content into catalog entries that can later drive batch download, evidence indexing, and distillation.

#### Scenario: Normalize enumerated video entry
- **WHEN** a creator content item is discovered during enumeration
- **THEN** the catalog entry stores at least a source key, source link or recoverable reference, title or visible label, publish-time value if available, publish-time precision, and discovery strategy

### Requirement: Enumeration completeness remains explicit
The system SHALL record enumeration completeness and failure reasons so a partial creator catalog is not misrepresented as complete.

#### Scenario: Record partial enumeration
- **WHEN** only part of a creator's visible content can be discovered in one run
- **THEN** the system records the creator catalog as partial and keeps the known failure reasons or blockers

