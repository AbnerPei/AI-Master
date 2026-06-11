export const TIMELINE_BLOCK = "ap-timeline";
export const ENTRY_SEPARATOR = "---";

export function createDefaultFormState(now = new Date()) {
  return {
    date: formatLocalDate(now),
    time: formatLocalTime(now),
    source: "",
    sourceUrl: "",
    heat: "",
    author: "",
    featured: false,
    featuredLabel: "",
    title: "",
    url: "",
    mediaSrc: "",
    mediaCaption: "",
    mediaAlt: "",
    mediaResume: false,
    tags: "",
    content: "",
    reason: "",
    discussions: "",
    note: "",
    images: []
  };
}

export function buildTimelineEntry(formState) {
  const entry = {};

  const date = normalizeText(formState.date);
  if (!date) {
    throw new Error("`date` 不能为空。");
  }
  entry.date = date;

  const time = normalizeText(formState.time);
  if (time) {
    entry.time = time;
  }

  assignIfPresent(entry, "source", formState.source);
  assignIfPresent(entry, "sourceUrl", formState.sourceUrl);
  assignIfPresent(entry, "heat", normalizeHeatValue(formState.heat));
  assignIfPresent(entry, "author", formState.author);

  if (formState.featured === true) {
    entry.featured = true;
  }
  assignIfPresent(entry, "featuredLabel", formState.featuredLabel);

  assignIfPresent(entry, "title", formState.title);
  assignIfPresent(entry, "url", formState.url);

  assignIfPresent(entry, "video", formState.mediaSrc);
  assignIfPresent(entry, "mediaCaption", formState.mediaCaption);
  assignIfPresent(entry, "mediaAlt", formState.mediaAlt);
  if (formState.mediaResume === true) {
    entry.isResume = true;
  }

  const tags = splitSimpleList(formState.tags);
  if (tags.length > 0) {
    entry.tags = tags;
  }

  assignIfPresent(entry, "content", formState.content);
  assignIfPresent(entry, "reason", formState.reason);
  assignIfPresent(entry, "discussions", formState.discussions);
  assignIfPresent(entry, "note", formState.note);

  const images = normalizeImageItems(formState.images);
  if (images.length > 0) {
    entry.images = images;
  }

  return entry;
}

export function serializeTimelineEntry(entry) {
  const lines = [];

  pushScalar(lines, "date", entry.date);
  pushScalar(lines, "time", entry.time);
  pushScalar(lines, "source", entry.source);
  pushScalar(lines, "sourceUrl", entry.sourceUrl);
  pushScalar(lines, "heat", entry.heat);
  pushScalar(lines, "author", entry.author);
  pushScalar(lines, "featured", entry.featured);
  pushScalar(lines, "featuredLabel", entry.featuredLabel);
  pushScalar(lines, "title", entry.title);
  pushScalar(lines, "url", entry.url);
  pushScalar(lines, "video", entry.video);
  pushBlock(lines, "mediaCaption", entry.mediaCaption);
  pushScalar(lines, "mediaAlt", entry.mediaAlt);
  pushScalar(lines, "isResume", entry.isResume);
  pushStringList(lines, "tags", entry.tags);
  pushBlock(lines, "content", entry.content);
  pushImageList(lines, entry.images);
  pushBlock(lines, "reason", entry.reason);
  pushBlock(lines, "discussions", entry.discussions);
  pushBlock(lines, "note", entry.note);

  return lines.join("\n").trim();
}

export function findTimelineBlocks(markdown) {
  const source = typeof markdown === "string" ? markdown : "";
  const blocks = [];
  const pattern = /```ap-timeline[^\n\r]*\r?\n([\s\S]*?)\r?\n```/g;
  let match;

  while ((match = pattern.exec(source)) !== null) {
    const content = match[1] ?? "";
    const contentStart = match.index + match[0].indexOf(content);
    const contentEnd = contentStart + content.length;
    blocks.push({
      index: blocks.length + 1,
      start: match.index,
      end: pattern.lastIndex,
      contentStart,
      contentEnd,
      content
    });
  }

  return blocks;
}

export function insertTimelineEntry(markdown, entryYaml, options = {}) {
  const source = typeof markdown === "string" ? markdown : "";
  const blockIndex = Math.max(1, Number(options.blockIndex ?? 1) || 1);
  const sortOrder = options.sortOrder === "asc" ? "asc" : "desc";
  const blocks = findTimelineBlocks(source);

  if (blocks.length === 0) {
    const trimmedEntry = entryYaml.trim();
    const blockText = [
      "```ap-timeline",
      ENTRY_SEPARATOR,
      trimmedEntry,
      "```"
    ].join("\n");
    const prefix = source.trim().length === 0
      ? ""
      : `${source.replace(/\s*$/, "")}\n\n`;
    return {
      markdown: `${prefix}${blockText}\n`,
      blockCount: 1,
      insertedBlockIndex: 1,
      createdBlock: true
    };
  }

  if (blockIndex > blocks.length) {
    throw new Error(`当前文件只有 ${blocks.length} 个 \`${TIMELINE_BLOCK}\` 代码块。`);
  }

  const targetBlock = blocks[blockIndex - 1];
  const docs = splitTimelineDocuments(targetBlock.content);
  const nextEntries = docs.map((doc, index) => ({
    raw: doc.trim(),
    sortKey: extractDocumentSortKey(doc),
    originalIndex: index
  }));

  nextEntries.push({
    raw: entryYaml.trim(),
    sortKey: extractDocumentSortKey(entryYaml),
    originalIndex: nextEntries.length
  });

  nextEntries.sort((left, right) => compareDocuments(left, right, sortOrder));
  const nextContent = nextEntries
    .filter((entry) => entry.raw.length > 0)
    .map((entry) => `${ENTRY_SEPARATOR}\n${entry.raw}`)
    .join("\n");

  const nextMarkdown = [
    source.slice(0, targetBlock.contentStart),
    nextContent,
    source.slice(targetBlock.contentEnd)
  ].join("");

  return {
    markdown: nextMarkdown,
    blockCount: blocks.length,
    insertedBlockIndex: blockIndex,
    createdBlock: false
  };
}

function splitTimelineDocuments(source) {
  const docs = [];
  let current = [];

  source.split(/\r?\n/).forEach((line) => {
    if (line.trim() === ENTRY_SEPARATOR) {
      const text = current.join("\n").trim();
      if (text) {
        docs.push(text);
      }
      current = [];
      return;
    }
    current.push(line);
  });

  const tail = current.join("\n").trim();
  if (tail) {
    docs.push(tail);
  }

  return docs;
}

function extractDocumentSortKey(documentText) {
  const date = extractYamlScalar(documentText, "date");
  const time = extractYamlScalar(documentText, "time");
  return computeSortKey(date, time);
}

function compareDocuments(left, right, sortOrder) {
  if (left.sortKey !== null && right.sortKey !== null && left.sortKey !== right.sortKey) {
    return sortOrder === "asc"
      ? left.sortKey - right.sortKey
      : right.sortKey - left.sortKey;
  }

  if (left.sortKey !== null && right.sortKey === null) {
    return -1;
  }

  if (left.sortKey === null && right.sortKey !== null) {
    return 1;
  }

  return left.originalIndex - right.originalIndex;
}

function extractYamlScalar(documentText, key) {
  const escapedKey = key.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = documentText.match(new RegExp(`^\\s*${escapedKey}:\\s*(.+?)\\s*$`, "m"));
  if (!match) {
    return null;
  }

  const rawValue = String(match[1] ?? "").trim();
  if (!rawValue || rawValue === "|" || rawValue === ">") {
    return null;
  }

  return unquoteYamlString(rawValue);
}

export function computeSortKey(date, time) {
  const normalizedDate = normalizeText(date);
  if (!normalizedDate) {
    return null;
  }

  const normalizedTime = normalizeText(time);
  const candidates = normalizedTime
    ? [
      `${normalizedDate}T${normalizedTime}`,
      `${normalizedDate} ${normalizedTime}`,
      normalizedDate
    ]
    : [normalizedDate];

  for (const candidate of candidates) {
    const timestamp = Date.parse(candidate);
    if (!Number.isNaN(timestamp)) {
      return timestamp;
    }
  }

  return null;
}

function pushScalar(lines, key, value) {
  if (value === undefined || value === null || value === "") {
    return;
  }

  if (typeof value === "boolean" || typeof value === "number") {
    lines.push(`${key}: ${String(value)}`);
    return;
  }

  lines.push(`${key}: ${yamlDoubleQuote(String(value))}`);
}

function pushBlock(lines, key, value) {
  const text = normalizeText(value, { keepNewlines: true });
  if (!text) {
    return;
  }

  lines.push(`${key}: |`);
  text.split("\n").forEach((line) => {
    lines.push(`  ${line}`);
  });
}

function pushStringList(lines, key, values) {
  if (!Array.isArray(values) || values.length === 0) {
    return;
  }

  lines.push(`${key}:`);
  values.forEach((value) => {
    lines.push(`  - ${yamlDoubleQuote(value)}`);
  });
}

function pushImageList(lines, images) {
  if (!Array.isArray(images) || images.length === 0) {
    return;
  }

  lines.push("images:");
  images.forEach((image) => {
    lines.push(`  - src: ${yamlDoubleQuote(image.src)}`);

    if (image.caption) {
      if (image.caption.includes("\n")) {
        lines.push("    caption: |");
        image.caption.split("\n").forEach((line) => {
          lines.push(`      ${line}`);
        });
      } else {
        lines.push(`    caption: ${yamlDoubleQuote(image.caption)}`);
      }
    }

    if (image.alt) {
      lines.push(`    alt: ${yamlDoubleQuote(image.alt)}`);
    }

    if (image.progress !== undefined && image.progress !== null && image.progress !== "") {
      lines.push(`    progress: ${String(image.progress)}`);
    }

    if (image.isProgressColorful === true) {
      lines.push("    isProgressColorful: true");
    }

    if (image.isResume === true) {
      lines.push("    isResume: true");
    }
  });
}

function normalizeImageItems(values) {
  if (!Array.isArray(values)) {
    return [];
  }

  return values
    .map((value) => {
      const src = normalizeText(value?.src);
      if (!src) {
        return null;
      }

      const item = { src };
      assignIfPresent(item, "caption", value?.caption);
      assignIfPresent(item, "alt", value?.alt);

      const progress = clampProgress(value?.progress);
      if (progress !== null) {
        item.progress = progress;
      }

      if (value?.isProgressColorful === true) {
        item.isProgressColorful = true;
      }

      if (value?.isResume === true) {
        item.isResume = true;
      }

      return item;
    })
    .filter(Boolean);
}

function assignIfPresent(target, key, value) {
  if (typeof value === "number" && Number.isFinite(value)) {
    target[key] = value;
    return;
  }

  if (typeof value === "boolean") {
    target[key] = value;
    return;
  }

  const normalized = normalizeText(value, { keepNewlines: true });
  if (normalized) {
    target[key] = normalized;
  }
}

function splitSimpleList(value) {
  const normalized = normalizeText(value, { keepNewlines: true });
  if (!normalized) {
    return [];
  }

  return normalized
    .split(/[\n,，]/)
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
}

function normalizeHeatValue(value) {
  const text = normalizeText(value);
  if (!text) {
    return null;
  }
  return /^-?\d+(?:\.\d+)?$/.test(text) ? Number(text) : text;
}

function clampProgress(value) {
  const text = normalizeText(value);
  if (!text) {
    return null;
  }
  const parsed = Number(text);
  if (!Number.isFinite(parsed)) {
    return null;
  }
  if (parsed < 1) {
    return 1;
  }
  if (parsed > 8) {
    return 8;
  }
  return parsed;
}

function normalizeText(value, options = {}) {
  if (typeof value !== "string") {
    if (typeof value === "number") {
      return String(value);
    }
    return "";
  }

  const normalized = value.replace(/\r\n/g, "\n");
  return options.keepNewlines === true ? normalized.trim() : normalized.trim();
}

function yamlDoubleQuote(value) {
  return JSON.stringify(String(value));
}

function unquoteYamlString(value) {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith("\"") && trimmed.endsWith("\""))
    || (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function formatLocalDate(date) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatLocalTime(date) {
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  return `${hours}:${minutes}`;
}
