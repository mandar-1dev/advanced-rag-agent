export default function MessageBubble({ role, text }) {
    const isUser = role === 'user'
    return (
        <div className={`rounded-3xl p-4 ${isUser ? 'bg-cyan-500/10 text-cyan-100 self-end' : 'bg-slate-800 text-slate-100'}`}>
            <p className="text-sm leading-6">{text}</p>
        </div>
    )
}
