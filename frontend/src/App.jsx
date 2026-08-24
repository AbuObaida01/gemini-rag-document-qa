import { useState } from "react";

import DocumentUpload from "./components/DocumentUpload";
import DocumentList from "./components/DocumentList";
import QueryBox from "./components/QueryBox";
import Answer from "./components/Answer";
import SourceList from "./components/SourceList";

import "./App.css";

function App() {
  const [refreshDocuments, setRefreshDocuments] =
    useState(0);

  const [queryResult, setQueryResult] =
    useState(null);

  const handleUploadSuccess = () => {
    setRefreshDocuments(
      (current) => current + 1
    );
  };

  const handleQueryResult = (result) => {
    setQueryResult(result);
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Gemini RAG</h1>

        <p>
          Ask questions about your uploaded
          documents.
        </p>
      </header>

      <main className="container">
        <DocumentUpload
          onUploadSuccess={
            handleUploadSuccess
          }
        />

        <DocumentList
          refreshTrigger={
            refreshDocuments
          }
        />

        <QueryBox
          onResult={handleQueryResult}
        />

        <Answer result={queryResult} />

        {queryResult && (
          <SourceList
            sources={
              queryResult.sources
            }
          />
        )}
      </main>
    </div>
  );
}

export default App;