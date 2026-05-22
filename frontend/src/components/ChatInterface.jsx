import { useState } from 'react'
import { useChat } from '../hooks/useChat'
import MessageBubble from './MessageBubble'
import FileUpload from './FileUpload'
import TypingIndicator from './TypingIndicator'

export default function ChatInterface() {
    const [input, setInput] = useState('')
    const { messages, loading, sendMessage } = useChat()

    const handleSubmit = async (event) => {
        event.preventDefault()
        if (!input.trim()) return
        await sendMessage(input.trim())
        setInput('')
    }

    return (
        <section className="flex-1 rounded-3xl bg-slate-900/90 p-6 shadow-2xl shadow-slate-950/20 backdrop-blur-xl">
            <h1 className="text-2xl font-semibold">Advanced RAG Agent</h1>
            <div className="mt-6 space-y-4 h-[60vh] overflow-y-auto pr-2">
                {messages.map((message, index) => (
                    <MessageBubble key={index} role={message.role} text={message.text} />
                ))}
                {loading && <TypingIndicator />}
            </div>
            <form onSubmit={handleSubmit} className="mt-4 flex gap-3">
                <input
                    value={input}
                    onChange={(event) => setInput(event.target.value)}
                    className="flex-1 rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 focus:border-cyan-400 focus:outline-none"
                    placeholder="Ask a question about your knowledge base..."
                />
                <button type="submit" className="rounded-2xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 hover:bg-cyan-400">
                    Send
                </button>
            </form>
            <FileUpload />
        </section>
    )
}
