import { useState } from "react";
import { queryDocuments } from "../services/api";

function QueryBox({
  onResult,
}) {
  const [question, setQuestion] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    const trimmedQuestion =
      question.trim();

    if (!trimmedQuestion) {
      setError(
        "Please enter a question."
      );
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result =
        await queryDocuments(
          trimmedQuestion
        );

      onResult(result);
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Failed to get an answer.";

      setError(message);
      onResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="card">
      <h2>Ask a Question</h2>

      <form onSubmit={handleSubmit}>
        <textarea
          value={question}
          onChange={(event) =>
            setQuestion(
              event.target.value
            )
          }
          placeholder="Ask a question about your documents..."
          rows={4}
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading}
        >
          {loading
            ? "Generating answer..."
            : "Ask Question"}
        </button>
      </form>

      {error && (
        <p className="error">
          {error}
        </p>
      )}
    </section>
  );
}

export default QueryBox;