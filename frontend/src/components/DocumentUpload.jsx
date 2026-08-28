import { useState } from "react";
import { uploadDocument } from "../services/api";

const ALLOWED_EXTENSIONS = [
  ".pdf",
  ".txt",
  ".md",
  ".docx",
  ".csv",
  ".xlsx",
  ".pptx",
  ".html",
  ".htm",
  ".json",
  ".png",
  ".jpg",
  ".jpeg",
  ".webp",
  ".tif",
  ".tiff",
];

const ACCEPTED_FILES = ALLOWED_EXTENSIONS.join(",");

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

    const extension = (
      "." + selectedFile.name.split(".").pop()
    ).toLowerCase();

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      setError(
        "Unsupported file format. Please select a supported document or image."
      );
      setFile(null);
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file.");
      return;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const result = await uploadDocument(file);

      setSuccess(
        `${result.document} uploaded successfully. ` +
        `${result.chunks_created} chunks processed.`
      );

      setFile(null);

      document.getElementById(
        "document-file-input"
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
        id="document-file-input"
        type="file"
        accept={ACCEPTED_FILES}
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
          ? "Processing..."
          : "Upload File"}
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