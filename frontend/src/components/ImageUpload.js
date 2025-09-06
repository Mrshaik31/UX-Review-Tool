
import React, { useState } from "react";
import { UploadCloud } from "lucide-react";

const ImageUpload = ({ onResults }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/api/analyze", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (!response.ok) {
        onResults({ error: data.error || "Upload failed" });
      } else {
        onResults(data);
      }
    } catch (error) {
      onResults({ error: "Network error or server not reachable" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center">
      {/* Upload Box */}
      <label
        htmlFor="file-input"
        className="w-full cursor-pointer flex flex-col items-center justify-center border-2 border-dashed border-indigo-400 dark:border-blue-300 rounded-2xl p-10 text-center transition hover:bg-indigo-50 dark:hover:bg-gray-700"
      >
        <UploadCloud className="w-12 h-12 text-indigo-500 dark:text-blue-300 mb-3" />
        <p className="text-gray-700 dark:text-gray-400 font-semibold">
          {selectedFile ? "Change file" : "Click to upload or drag & drop"}
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          PNG, JPG up to 5MB
        </p>
        <input
          id="file-input"
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />
      </label>

      {/* Preview */}
      {preview && (
        <div className="mt-6 w-full">
          <img
            src={preview}
            alt="Preview"
            className="w-full max-h-64 object-contain rounded-xl border shadow-md"
          />
        </div>
      )}

      {/* Upload Button */}
      <button
        onClick={handleUpload}
        disabled={!selectedFile || loading}
        className={`mt-6 w-full py-3 px-6 rounded-xl font-semibold shadow-md transition ${
          !selectedFile || loading
            ? "bg-gray-300 text-gray-500 cursor-not-allowed"
            : "bg-blue-400 hover:bg-blue-500 text-black:bg-indigo-500 hover:bg-indigo-600 text-white"
        }`}
      >
        {loading ? "Analyzing..." : "Analyze UX"}
      </button>
    </div>
  );
};

export default ImageUpload;
