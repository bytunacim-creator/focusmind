import "@testing-library/jest-dom/vitest";

if (!globalThis.crypto || typeof globalThis.crypto.randomUUID !== "function") {
  globalThis.crypto = globalThis.crypto ?? {};
  let counter = 0;
  globalThis.crypto.randomUUID = () => `test-uuid-${counter++}`;
}
