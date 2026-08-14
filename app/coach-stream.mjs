export const MAX_COACH_STREAM_BYTES = 128_000;
export const MAX_COACH_STREAM_PENDING_CHARS = 16_000;

/** Parse KitCode's small provider-neutral SSE protocol with bounded buffering. */
export async function readCoachStream(response, onEvent, shouldContinue = () => true) {
  if (!response.body) throw new Error("The coach did not open a streaming response.");
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let pending = "";
  let eventName = "message";
  let dataLines = [];
  const dispatch = () => {
    if (!dataLines.length) {
      eventName = "message";
      return;
    }
    const raw = dataLines.join("\n");
    dataLines = [];
    try {
      const payload = JSON.parse(raw);
      if (eventName === "delta" && typeof payload.delta === "string")
        onEvent({ type: "delta", delta: payload.delta });
      else if (eventName === "meta" || eventName === "done")
        onEvent({ type: eventName, provider: typeof payload.provider === "string" ? payload.provider : undefined, model: typeof payload.model === "string" ? payload.model : undefined });
      else if (eventName === "error")
        onEvent({ type: "error", message: typeof payload.message === "string" ? payload.message : "The coach stream stopped unexpectedly.", status: typeof payload.status === "number" ? payload.status : undefined });
    } catch {
      throw new Error("The coach sent an unreadable streaming response.");
    } finally {
      eventName = "message";
    }
  };
  let receivedBytes = 0;
  try {
    while (true) {
      if (!shouldContinue()) throw new Error("The coach request is no longer current.");
      const { value, done } = await reader.read();
      receivedBytes += value?.byteLength ?? 0;
      if (receivedBytes > MAX_COACH_STREAM_BYTES)
        throw new Error("The coach response was too large to display safely.");
      pending += decoder.decode(value ?? new Uint8Array(), { stream: !done });
      if (pending.length > MAX_COACH_STREAM_PENDING_CHARS)
        throw new Error("The coach sent an incomplete response that was too large to display safely.");
      const lines = pending.split(/\r?\n/);
      pending = lines.pop() ?? "";
      for (const line of lines) {
        if (!shouldContinue()) throw new Error("The coach request is no longer current.");
        if (!line) dispatch();
        else if (line.startsWith("event:")) eventName = line.slice(6).trim();
        else if (line.startsWith("data:")) dataLines.push(line.slice(5).trimStart());
      }
      if (done) break;
    }
    if (pending) {
      if (pending.startsWith("event:")) eventName = pending.slice(6).trim();
      else if (pending.startsWith("data:")) dataLines.push(pending.slice(5).trimStart());
    }
    dispatch();
  } finally {
    await reader.cancel().catch(() => undefined);
  }
}
