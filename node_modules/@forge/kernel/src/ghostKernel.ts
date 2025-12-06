import { create } from "zustand";

export type ForgeMode = "ghost" | "kernel" | "duress";

interface KernelState {
  mode: ForgeMode;
  lastEventAt: number;
  setMode: (mode: ForgeMode) => void;
  touch: () => void;
}

export const useKernelStore = create<KernelState>((set) => ({
  mode: "ghost",
  lastEventAt: Date.now(),
  setMode: (mode) => set({ mode }),
  touch: () => set({ lastEventAt: Date.now() })
}));

export function isAuthenticated(mode: ForgeMode): boolean {
  return mode === "kernel";
}
