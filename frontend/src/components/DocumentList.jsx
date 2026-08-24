import { useEffect, useState } from "react";
import {
  deleteDocument,
  getDocuments,
} from "../services/api";

function DocumentList({
  refreshTrigger,
}) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDocuments = async () => {
    setLoading(true);
    setError("");

    try {
      const result = await getDocuments();

      setDocuments(result.documents || []);
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Failed to load documents.";

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, [refreshTrigger]);

  const handleDelete = async (documentName) => {
    const confirmed = window.confirm(
      `Delete "${documentName}"?`
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteDocument(documentName);

      setDocuments((current) =>
        current.filter(
          (document) =>
            document !== documentName
        )
      );
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Failed to delete document.";

      setError(message);
    }
  };

  return (
    <section className="card">
      <div className="section-header">
        <h2>Documents</h2>

        <button
          className="secondary-button"
          onClick={loadDocuments}
        >
          Refresh
        </button>
      </div>

      {loading && (
        <p>Loading documents...</p>
      )}

      {error && (
        <p className="error">{error}</p>
      )}

      {!loading &&
        documents.length === 0 && (
          <p>
            No documents have been uploaded yet.
          </p>
        )}

      {!loading &&
        documents.length > 0 && (
          <div className="document-list">
            {documents.map((document) => (
              <div
                className="document-item"
                key={document}
              >
                <span>{document}</span>

                <button
                  className="danger-button"
                  onClick={() =>
                    handleDelete(document)
                  }
                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
    </section>
  );
}

export default DocumentList;