import { useState } from 'react'

export function useUpload() {
    const [uploadStatus, setUploadStatus] = useState('No file uploaded yet.')

    const handleFileChange = async (event) => {
        const file = event.target.files?.[0]
        if (!file) {
            setUploadStatus('No file selected.')
            return
        }

        setUploadStatus(`Selected file: ${file.name}`)
        // TODO: implement actual upload logic to backend
    }

    return { handleFileChange, uploadStatus }
}
