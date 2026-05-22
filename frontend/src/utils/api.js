const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
const API_TIMEOUT = 65000  // 65 seconds (slightly more than backend timeout)

export async function queryAgent(payload) {
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT)
    
    try {
        const response = await fetch(`${API_BASE}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            signal: controller.signal,
        })
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: response.statusText }))
            throw new Error(errorData.detail || `HTTP ${response.status}`)
        }
        
        return await response.json()
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timed out. The server took too long to respond.')
        }
        throw error
    } finally {
        clearTimeout(timeoutId)
    }
}
