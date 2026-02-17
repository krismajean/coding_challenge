// Background service worker that periodically fetches the latest names
// from the Wikipedia article and caches them in chrome.storage.local.

const WIKI_API_URL =
  "https://en.wikipedia.org/w/api.php?action=parse&page=List_of_people_named_in_the_Epstein_files&prop=sections&format=json&origin=*";

const WIKI_ARTICLE_URL =
  "https://en.wikipedia.org/w/api.php?action=parse&page=List_of_people_named_in_the_Epstein_files&prop=text&format=json&origin=*";

const CACHE_KEY = "epstein_names_cache";
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

// Fetch section list from Wikipedia API to discover person-name headings
async function fetchNamesFromWiki() {
  try {
    // Step 1: Get all sections
    const sectionsResp = await fetch(WIKI_API_URL);
    if (!sectionsResp.ok) return null;
    const sectionsData = await sectionsResp.json();
    const sections = sectionsData?.parse?.sections || [];

    // Person names are typically level-3 headings (=== Name ===)
    // which appear as toclevel 3 or level "3" in the API response
    const personSections = sections.filter(
      (s) => parseInt(s.level) === 3 || parseInt(s.toclevel) === 3
    );

    if (personSections.length === 0) return null;

    const names = personSections.map((s) => ({
      name: s.line.replace(/<[^>]*>/g, "").trim(), // strip any HTML tags
      anchor: s.anchor,
    }));

    return names;
  } catch (err) {
    console.warn("[Sunshine] Failed to fetch from Wikipedia:", err);
    return null;
  }
}

// Update cache if stale
async function maybeUpdateCache() {
  const stored = await chrome.storage.local.get(CACHE_KEY);
  const cache = stored[CACHE_KEY];

  if (cache && Date.now() - cache.timestamp < CACHE_TTL_MS) {
    return; // Cache is fresh
  }

  const names = await fetchNamesFromWiki();
  if (names && names.length > 0) {
    await chrome.storage.local.set({
      [CACHE_KEY]: {
        names,
        timestamp: Date.now(),
      },
    });
    console.log(
      `[Sunshine] Cached ${names.length} names from Wikipedia`
    );
  }
}

// Run on install and periodically
chrome.runtime.onInstalled.addListener(() => {
  maybeUpdateCache();
});

// Check every 6 hours
chrome.alarms.create("updateNames", { periodInMinutes: 360 });
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "updateNames") {
    maybeUpdateCache();
  }
});

// Allow content script to request the latest names
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "getNames") {
    chrome.storage.local.get(CACHE_KEY).then((stored) => {
      sendResponse(stored[CACHE_KEY]?.names || null);
    });
    return true; // async response
  }
});
