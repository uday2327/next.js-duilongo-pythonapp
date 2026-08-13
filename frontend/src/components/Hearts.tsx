export function Hearts({ count }: { count: number }) {
  return <div className="font-black text-rose-500">{"Heart ".repeat(Math.max(0, count)).trim() || "No hearts"}</div>;
}
