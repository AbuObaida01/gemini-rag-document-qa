import { useState } from "react";
import { uploadDocument } from "../services/api";

function DocumentUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    setError("");
    setSuccess("");

    if (!selectedFile) {
      setFile(null);
      return;
    }

    if (
      selectedFile.type !== "application/pdf"
    ) {
      setError("Only PDF files are allowed.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const result = await uploadDocument(file);

      setSuccess(
        `${result.document} uploaded successfully. ` +
        `${result.pages_extracted} pages and ` +
        `${result.chunks_created} chunks processed.`
      );

      setFile(null);

      document.getElementById(
        "pdf-file-input"
      ).value = "";

      if (onUploadSuccess) {
        onUploadSuccess();
      }
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Failed to upload document.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Upload Document</h2>

      <input
        id="pdf-file-input"
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleFileChange}
        disabled={loading}
      />

      {file && (
        <p className="selected-file">
          Selected: {file.name}
        </p>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading
          ? "Processing document..."
          : "Upload PDF"}
      </button>

      {success && (
        <p className="success">
          {success}
        </p>
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}
    </section>
  );
}

export default DocumentUpload;