import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import AttentionTest from "../components/AttentionTest.jsx";

beforeEach(() => {
  vi.useFakeTimers();
  vi.stubGlobal("requestAnimationFrame", (cb) => cb());
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("AttentionTest", () => {
  it("shows instructions before starting", () => {
    render(<AttentionTest onComplete={() => {}} />);
    expect(screen.getByText(/Teste Başla/)).toBeInTheDocument();
  });

  it("enters running phase on start, before ISI elapses", () => {
    render(<AttentionTest onComplete={() => {}} />);
    fireEvent.click(screen.getByText(/Teste Başla/));
    expect(screen.getByText(/Hazır olun/)).toBeInTheDocument();
  });

  it("presents a go or no-go stimulus once ISI elapses", () => {
    render(<AttentionTest onComplete={() => {}} />);
    fireEvent.click(screen.getByText(/Teste Başla/));
    act(() => { vi.advanceTimersByTime(2000); }); // MAX_ISI_MS = 1800
    const goStimulus = screen.queryByTestId("go-stimulus");
    const noGoStimulus = screen.queryByTestId("no-go-stimulus");
    expect(goStimulus || noGoStimulus).toBeTruthy();
  });
});
