document.getElementById("query-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const query = document.getElementById("query").value;
  const output = document.getElementById("output");
  const source = document.getElementById("source");

  output.innerHTML = "";
  source.innerHTML = "";

  const response = await fetch("/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    output.innerHTML = "<strong>Error:</strong> Unable to get summary.";
    return;
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });

    chunk.split("\n\n").forEach((line) => {
      if (line.startsWith("data:")) {
        const content = line.replace("data: ", "");

        if (content.startsWith("[SOURCE_URL]")) {
          const url = content.replace("[SOURCE_URL]", "").trim();
          source.innerHTML = `<a href="${url}" target="_blank">Source</a>`;
        } else {
          buffer += content;
          output.innerHTML = marked.parse(buffer);  // ✅ stream + markdown render
        }
      }
    });
  }
});