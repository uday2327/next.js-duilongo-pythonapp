export function ProgressRing({ progress, children }: { progress: number; children: React.ReactNode }) {
  return (
    <div
      className="grid h-24 w-24 place-items-center rounded-full"
      style={{ background: `conic-gradient(#ffc800 ${progress * 3.6}deg, #e5e7eb 0deg)` }}
    >
      <div className="grid h-20 w-20 place-items-center rounded-full bg-white shadow-inner">{children}</div>
    </div>
  );
}
