import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
});

export const uploadDocument = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/api/documents/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const getDocuments = async () => {
  const response = await api.get(
    "/api/documents"
  );

  return response.data;
};

export const deleteDocument = async (
  documentName
) => {
  const response = await api.delete(
    `/api/documents/${encodeURIComponent(
      documentName
    )}`
  );

  return response.data;
};

export const queryDocuments = async (
  question
) => {
  const response = await api.post(
    "/api/query",
    {
      question,
    }
  );

  return response.data;
};

export default api;