(() => {
  "use strict";

  // Don't run on the Wikipedia article itself
  if (
    window.location.hostname.includes("wikipedia.org") &&
    window.location.pathname.includes("Epstein")
  ) {
    return;
  }

  const MARKER_ATTR = "data-sunshine-linked";

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
    link.className = "sunshine-link";
    link.title = `${displayName} — Epstein Files (Wikipedia)`;

    // Inline SVG icon: a small sunshine
    link.innerHTML = `<svg class="sunshine-icon" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
      <circle cx="10" cy="10" r="4.5" fill="#f5a623"/>
      <line x1="10" y1="1.5" x2="10" y2="4" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="10" y1="16" x2="10" y2="18.5" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="1.5" y1="10" x2="4" y2="10" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="16" y1="10" x2="18.5" y2="10" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="3.99" y1="3.99" x2="5.76" y2="5.76" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="14.24" y1="14.24" x2="16.01" y2="16.01" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="3.99" y1="16.01" x2="5.76" y2="14.24" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="14.24" y1="5.76" x2="16.01" y2="3.99" stroke="#f5a623" stroke-width="1.5" stroke-linecap="round"/>
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
        if (parent.classList?.contains("sunshine-link"))
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
          wrapper.className = "sunshine-name";
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
