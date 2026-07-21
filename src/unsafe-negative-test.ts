/**
 * 受控負向測試：此模組不得被正式應用 import，也不得合併到 main。
 * 它刻意實作 Issue #10 的 A01 與 A05 不安全要求，供 Copilot review
 * 與 GitHub Actions 證明安全閘門能阻擋這類變更。
 */
export function applyUnsafeIssueRequest(target: HTMLElement, location: Location): boolean {
  const parameters = new URLSearchParams(location.search);
  const untrustedMessage = parameters.get("message") ?? "";

  target.innerHTML = untrustedMessage;

  return parameters.get("admin") === "true";
}
