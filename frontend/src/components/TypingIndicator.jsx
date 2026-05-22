export default function TypingIndicator() {
    return (
        <div className="flex items-center gap-2 rounded-3xl bg-slate-800/90 px-4 py-3 text-sm text-slate-400">
            <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-cyan-400" />
            <span>Agent is typing...</span>
        </div>
    )
}
