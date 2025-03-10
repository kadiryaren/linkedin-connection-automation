chrome.webRequest.onBeforeRequest.addListener(
  function(details) {
    return { cancel: details.url.includes("ttvnw.net") };
  },
  { urls: ["<all_urls>"] },
  ["blocking"]
);

// chrome.webRequest.onBeforeRequest.addListener(
//   function(details) {
//     return { cancel: details.url.includes("gql.twitch.tv") };
//   },
//   { urls: ["<all_urls>"] },
//   ["blocking"]
// );