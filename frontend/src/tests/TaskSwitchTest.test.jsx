import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import TaskSwitchTest from "../components/TaskSwitchTest.jsx";

beforeEach(() => {
  vi.useFakeTimers();
  vi.stubGlobal("requestAnimationFrame", (cb) => cb());
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("TaskSwitchTest", () => {
  it("shows instructions before starting", () => {
    render(<TaskSwitchTest onComplete={() => {}} />);
    expect(screen.getByText(/Teste Başla/)).toBeInTheDocument();
  });

  it("shows the active rule cue and both response buttons after ISI elapses", () => {
    render(<TaskSwitchTest onComplete={() => {}} />);
    fireEvent.click(screen.getByText(/Teste Başla/));
    act(() => { vi.advanceTimersByTime(1500); }); // MAX_ISI_MS = 1400
    expect(screen.getByTestId("rule-cue")).toBeInTheDocument();
    expect(screen.getByText("Buton 1")).toBeInTheDocument();
    expect(screen.getByText("Buton 2")).toBeInTheDocument();
    expect(screen.getByTestId("switch-stimulus")).toBeInTheDocument();
  });

  it("first trial's rule cue is 'RENK' (block sequence starts with color)", () => {
    render(<TaskSwitchTest onComplete={() => {}} />);
    fireEvent.click(screen.getByText(/Teste Başla/));
    act(() => { vi.advanceTimersByTime(1500); });
    expect(screen.getByTestId("rule-cue").textContent).toMatch(/RENK/);
  });
});
