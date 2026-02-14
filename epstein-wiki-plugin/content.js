(() => {
  "use strict";

  // Don't run on the Wikipedia article itself
  if (
    window.location.hostname.includes("wikipedia.org") &&
    window.location.pathname.includes("Epstein")
  ) {
    return;
  }

  const MARKER_ATTR = "data-epstein-wiki-linked";

  // Build a lookup: lowercase name/alias -> { anchor, displayName }
  function buildLookup(namesList) {
    const lookup = new Map();
    for (const entry of namesList) {
      const allNames = [entry.name, ...(entry.aliases || [])];
      for (const n of allNames) {
        lookup.set(n.toLowerCase(), {
          anchor: entry.anchor,
          displayName: entry.name,
        });
      }
    }
    return lookup;
  }

  // Build regex from a lookup map
  function buildPattern(lookup) {
    const allNameStrings = [...lookup.keys()].sort(
      (a, b) => b.length - a.length
    );
    return new RegExp(
      "\\b(" + allNameStrings.map(escapeRegex).join("|") + ")\\b",
      "gi"
    );
  }

  // Escape regex special chars
  function escapeRegex(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  // Create the small wiki-link icon element
  function createIcon(anchor, displayName) {
    const link = document.createElement("a");
    link.href = `${WIKI_BASE_URL}#${anchor}`;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.className = "epstein-wiki-link";
    link.title = `${displayName} — Epstein Files (Wikipedia)`;

    // Inline SVG icon: a small "W" in a circle
    link.innerHTML = `<svg class="epstein-wiki-icon" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
      <circle cx="10" cy="10" r="9" fill="#36c" stroke="#fff" stroke-width="1"/>
      <text x="10" y="14.5" text-anchor="middle" fill="#fff" font-size="11" font-family="serif" font-weight="bold">W</text>
    </svg>`;

    return link;
  }

  // Tags we should never scan inside
  const SKIP_TAGS = new Set([
    "SCRIPT",
    "STYLE",
    "TEXTAREA",
    "INPUT",
    "SELECT",
    "NOSCRIPT",
    "IFRAME",
    "SVG",
    "CODE",
    "PRE",
  ]);

  // Walk text nodes in the DOM and wrap matches
  function processNode(root, nameLookup, pattern) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode(node) {
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        if (parent.closest(`[${MARKER_ATTR}]`)) return NodeFilter.FILTER_REJECT;
        if (parent.classList?.contains("epstein-wiki-link"))
          return NodeFilter.FILTER_REJECT;
        if (SKIP_TAGS.has(parent.tagName)) return NodeFilter.FILTER_REJECT;
        if (parent.isContentEditable) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });

    const textNodes = [];
    while (walker.nextNode()) {
      textNodes.push(walker.currentNode);
    }

    for (const textNode of textNodes) {
      const text = textNode.nodeValue;
      if (!text || text.trim().length < 3) continue;

      // Reset regex state
      pattern.lastIndex = 0;

      const matches = [];
      let match;
      while ((match = pattern.exec(text)) !== null) {
        matches.push({
          index: match.index,
          length: match[0].length,
          matchedText: match[0],
        });
      }

      if (matches.length === 0) continue;

      // Replace text node with fragments containing highlighted names + icons
      const frag = document.createDocumentFragment();
      let lastIdx = 0;

      for (const m of matches) {
        // Text before the match
        if (m.index > lastIdx) {
          frag.appendChild(
            document.createTextNode(text.slice(lastIdx, m.index))
          );
        }

        const info = nameLookup.get(m.matchedText.toLowerCase());
        if (info) {
          const wrapper = document.createElement("span");
          wrapper.setAttribute(MARKER_ATTR, "true");
          wrapper.className = "epstein-wiki-name";
          wrapper.textContent = m.matchedText;
          wrapper.appendChild(createIcon(info.anchor, info.displayName));
          frag.appendChild(wrapper);
        } else {
          frag.appendChild(document.createTextNode(m.matchedText));
        }

        lastIdx = m.index + m.length;
      }

      // Remaining text after last match
      if (lastIdx < text.length) {
        frag.appendChild(document.createTextNode(text.slice(lastIdx)));
      }

      textNode.parentNode.replaceChild(frag, textNode);
    }
  }

  // --- Main logic ---

  // Start with the hardcoded names (from names.js)
  let nameLookup = buildLookup(EPSTEIN_NAMES);
  let pattern = buildPattern(nameLookup);

  // Initial scan with hardcoded names
  processNode(document.body, nameLookup, pattern);

  // Set up MutationObserver for dynamic content
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      for (const node of mutation.addedNodes) {
        if (node.nodeType === Node.ELEMENT_NODE) {
          processNode(node, nameLookup, pattern);
        }
      }
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });

  // Try to get updated names from the background service worker (fetched from Wikipedia)
  if (typeof chrome !== "undefined" && chrome.runtime?.sendMessage) {
    chrome.runtime.sendMessage({ type: "getNames" }, (liveNames) => {
      if (!liveNames || liveNames.length === 0) return;

      // Merge live names into the lookup (live names supplement the hardcoded ones)
      for (const entry of liveNames) {
        const key = entry.name.toLowerCase();
        if (!nameLookup.has(key)) {
          nameLookup.set(key, {
            anchor: entry.anchor,
            displayName: entry.name,
          });
        }
      }

      // Rebuild the regex with the expanded name list
      pattern = buildPattern(nameLookup);

      // Re-scan the page for any newly added names
      processNode(document.body, nameLookup, pattern);
    });
  }
})();
