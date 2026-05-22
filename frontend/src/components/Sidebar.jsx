export default function Sidebar() {
    return (
        <aside className="w-full max-w-sm rounded-3xl bg-slate-900/90 p-6 shadow-2xl shadow-slate-950/20 backdrop-blur-xl lg:w-80">
            <div className="space-y-4">
                <div>
                    <h2 className="text-xl font-semibold">Agent Controls</h2>
                    <p className="mt-2 text-sm text-slate-400">Upload files, query your RAG pipeline, and inspect sources.</p>
                </div>
                <div className="rounded-3xl border border-slate-800 bg-slate-950/60 p-4">
                    <p className="text-sm text-slate-500">Ready to explore retrieval-augmented generation with hybrid search and cross-encoder reranking.</p>
                </div>
            </div>
        </aside>
    )
}
