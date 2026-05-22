export default function SourceCard({ title, snippet }) {
    return (
        <div className="rounded-3xl border border-slate-800 bg-slate-950/80 p-4">
            <h3 className="font-semibold text-slate-100">{title}</h3>
            <p className="mt-2 text-sm text-slate-400">{snippet}</p>
        </div>
    )
}
