import { useEffect, useState } from 'react'
import api from '../services/api'
import { useAuthStore } from '../store/authStore'

export default function Files() {
  const [files, setFiles] = useState([])
  const [selectedFile, setSelectedFile] = useState(null)
  const [error, setError] = useState('')
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)

  const loadFiles = async () => {
    try {
      const resp = await api.get('/files/')
      setFiles(resp.data)
    } catch (err) {
      setError('Could not load files')
    }
  }

  useEffect(() => {
    loadFiles()
  }, [])

  const handleUpload = async (e) => {
    e.preventDefault()
    if (!selectedFile) return
    const formData = new FormData()
    formData.append('upload', selectedFile)
    try {
      await api.post('/files/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setSelectedFile(null)
      loadFiles()
    } catch (err) {
      setError('Upload failed')
    }
  }

  const handleDownload = async (file) => {
    const resp = await api.get(`/files/${file.id}`, { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([resp.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.original_filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
  }

  const handleDelete = async (file) => {
    await api.delete(`/files/${file.id}`)
    loadFiles()
  }

  return (
    <div className="files-page">
      <header>
        <h1>My Files</h1>
        <div>
          <span>{user?.email}</span>
          <button onClick={logout}>Log Out</button>
        </div>
      </header>

      <form onSubmit={handleUpload}>
        <input type="file" onChange={(e) => setSelectedFile(e.target.files[0])} />
        <button type="submit" disabled={!selectedFile}>Upload</button>
      </form>

      {error && <p className="error">{error}</p>}

      <ul className="file-list">
        {files.map((file) => (
          <li key={file.id}>
            <span>{file.original_filename}</span>
            <span>{file.file_size} bytes</span>
            <button onClick={() => handleDownload(file)}>Download</button>
            <button onClick={() => handleDelete(file)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  )
}