export default function Loading() {
  return (
    <main className="grid min-h-screen place-items-center bg-[var(--background)] px-4 text-center">
      <div className="pop-in">
        <div className="mx-auto h-14 w-14 animate-bounce rounded-full border-b-4 border-accent bg-accent" />
        <p className="mt-5 text-sm font-black uppercase tracking-wide text-muted">Loading</p>
      </div>
    </main>
  );
}
