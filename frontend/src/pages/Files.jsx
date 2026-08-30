import { useEffect, useRef, useState } from "react";
import api from "../services/api.js";
import { useAuthStore } from "../store/authStore.js";

function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const exponent = Math.min(
    Math.floor(Math.log(bytes) / Math.log(1024)),
    units.length - 1
  );
  const value = bytes / 1024 ** exponent;
  return `${value.toFixed(exponent === 0 ? 0 : 1)} ${units[exponent]}`;
}

export default function Files() {
  const logout = useAuthStore((state) => state.logout);
  const user = useAuthStore((state) => state.user);
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  async function loadFiles() {
    setLoading(true);
    try {
      const { data } = await api.get("/files/");
      setFiles(data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load files.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadFiles();
  }, []);

  async function handleUpload(event) {
    const selected = event.target.files?.[0];
    if (!selected) return;

    setError("");
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", selected);
      await api.post("/files/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      await loadFiles();
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  }

  async function handleDownload(file) {
    try {
      const response = await api.get(`/files/${file.id}/download`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", file.original_filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.response?.data?.detail || "Download failed.");
    }
  }

  async function handleDelete(file) {
    try {
      await api.delete(`/files/${file.id}`);
      await loadFiles();
    } catch (err) {
      setError(err.response?.data?.detail || "Delete failed.");
    }
  }

  return (
    <div className="files-page">
      <header className="files-header">
        <h1>My Files</h1>
        <div>
          {user && <span className="user-email">{user.email}</span>}
          <button type="button" onClick={logout}>
            Log out
          </button>
        </div>
      </header>

      {error && <p className="error">{error}</p>}

      <div className="upload-row">
        <input
          ref={fileInputRef}
          type="file"
          onChange={handleUpload}
          disabled={uploading}
        />
        {uploading && <span>Uploading...</span>}
      </div>

      {loading ? (
        <p>Loading files...</p>
      ) : files.length === 0 ? (
        <p>No files uploaded yet.</p>
      ) : (
        <table className="files-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Size</th>
              <th>Uploaded</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {files.map((file) => (
              <tr key={file.id}>
                <td>{file.original_filename}</td>
                <td>{formatBytes(file.file_size)}</td>
                <td>{new Date(file.created_at).toLocaleString()}</td>
                <td>
                  <button type="button" onClick={() => handleDownload(file)}>
                    Download
                  </button>
                  <button type="button" onClick={() => handleDelete(file)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
