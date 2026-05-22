import { useUpload } from '../hooks/useUpload'

export default function FileUpload() {
    const { handleFileChange, uploadStatus } = useUpload()

    return (
        <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-950/70 p-4">
            <label className="flex cursor-pointer flex-col gap-2 rounded-3xl border border-dashed border-slate-700 bg-slate-900/80 p-5 text-center text-slate-300 hover:border-cyan-400">
                <span>Upload a PDF or document to enrich the dataset.</span>
                <input type="file" accept="application/pdf" onChange={handleFileChange} className="hidden" />
            </label>
            <p className="mt-3 text-sm text-slate-500">{uploadStatus}</p>
        </div>
    )
}
