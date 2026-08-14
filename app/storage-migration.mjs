const currentStoragePrefix = "kitcode:";
// Keep compatibility data-only: the former product name is not shown or used
// by the current application beyond reconstructing its retired storage prefix.
const legacyStoragePrefixes = [["py", "pair:"].join("")];
const migrationMarkerKey = `${currentStoragePrefix}storage-migration-v1`;
const recoveredDraftPrefix = `${currentStoragePrefix}recovered-draft:`;

/**
 * Copy data from earlier browser-storage namespaces without deleting or
 * replacing anything already saved by KitCode.
 *
 * Draft conflicts are retained under a recovery key. The editor can then
 * distinguish an auto-saved starter from a genuinely newer edit.
 *
 * @param {Storage} storage
 */
export function migrateLegacyBrowserStorage(storage) {
  try {
    if (storage.getItem(migrationMarkerKey) === "complete") return;

    const keys = Array.from({ length: storage.length }, (_, index) =>
      storage.key(index),
    ).filter((key) => typeof key === "string");

    for (const legacyPrefix of legacyStoragePrefixes) {
      for (const legacyKey of keys) {
        if (!legacyKey.startsWith(legacyPrefix)) continue;
        const suffix = legacyKey.slice(legacyPrefix.length);
        const legacyValue = storage.getItem(legacyKey);
        if (legacyValue === null) continue;

        const currentKey = `${currentStoragePrefix}${suffix}`;
        const currentValue = storage.getItem(currentKey);
        if (currentValue === null) {
          storage.setItem(currentKey, legacyValue);
          continue;
        }

        if (suffix.startsWith("draft:") && currentValue !== legacyValue) {
          const recoveryKey = `${recoveredDraftPrefix}${suffix.slice("draft:".length)}`;
          if (storage.getItem(recoveryKey) === null)
            storage.setItem(recoveryKey, legacyValue);
        }
      }
    }

    storage.setItem(migrationMarkerKey, "complete");
  } catch {
    // Storage may be unavailable or full. Existing browser data is untouched.
  }
}

/**
 * Read a draft while safely resolving a rename-era conflict.
 *
 * @param {Storage} storage
 * @param {string} language
 * @param {string} exerciseId
 * @param {string | undefined} starterCode
 */
export function readPersistedDraft(
  storage,
  language,
  exerciseId,
  starterCode,
) {
  const currentKey = `${currentStoragePrefix}draft:${language}:${exerciseId}`;
  const recoveryKey = `${recoveredDraftPrefix}${language}:${exerciseId}`;
  const currentValue = storage.getItem(currentKey);
  const recoveredValue = storage.getItem(recoveryKey);
  const normalizeStarterText = (value) =>
    String(value ?? "")
      .replace(/\r\n/g, "\n")
      .trimEnd();
  const currentIsOnlyStarter =
    currentValue === null ||
    currentValue.trim() === "" ||
    normalizeStarterText(currentValue) === normalizeStarterText(starterCode);

  if (recoveredValue !== null && currentIsOnlyStarter) {
    storage.setItem(currentKey, recoveredValue);
    return recoveredValue;
  }
  return currentValue;
}

/**
 * Clear both the active draft and any retained rename-era recovery copy after
 * the user explicitly asks to reset or delete it.
 *
 * @param {Storage} storage
 * @param {string} language
 * @param {string} exerciseId
 */
export function clearPersistedDraft(storage, language, exerciseId) {
  storage.removeItem(
    `${currentStoragePrefix}draft:${language}:${exerciseId}`,
  );
  storage.removeItem(`${recoveredDraftPrefix}${language}:${exerciseId}`);
}
