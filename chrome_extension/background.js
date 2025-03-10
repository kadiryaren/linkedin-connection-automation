chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    return { cancel: details.url.includes("onyx.chanteney.cloudfront.hls.ttvnw.net") };
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);