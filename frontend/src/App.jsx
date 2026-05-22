import ChatInterface from './components/ChatInterface'
import Sidebar from './components/Sidebar'
import ParticleBackground from './components/ParticleBackground'

function App() {
    return (
        <div className="min-h-screen bg-slate-950 text-slate-100">
            <ParticleBackground />
            <div className="relative mx-auto flex max-w-6xl flex-col gap-6 p-6 lg:flex-row">
                <Sidebar />
                <ChatInterface />
            </div>
        </div>
    )
}

export default App
