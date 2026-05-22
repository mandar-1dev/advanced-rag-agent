import { useState } from 'react'
import { queryAgent } from '../utils/api'

export function useChat() {
    const [messages, setMessages] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    async function sendMessage(query) {
        setLoading(true)
        setError(null)
        try {
            const response = await queryAgent({ query, documents: [] })
            
            if (response.error || response.detail) {
                setError(response.detail || response.error)
                setMessages((prev) => [...prev, { role: 'user', text: query }, { role: 'error', text: response.detail || response.error }])
            } else {
                const answerText = response.results?.[0]?.answer || 'No response'
                setMessages((prev) => [...prev, { role: 'user', text: query }, { role: 'assistant', text: answerText }])
            }
        } catch (err) {
            const errorMsg = err.message || 'Failed to get response'
            setError(errorMsg)
            setMessages((prev) => [...prev, { role: 'user', text: query }, { role: 'error', text: errorMsg }])
        } finally {
            setLoading(false)
        }
    }

    return { messages, loading, error, sendMessage }
}
