import React from "react";

export default function FileUpload({ onFile, accept = ".docx" }) {
  return (
    <div>
      <label>Resume File</label>
      <input
        type="file"
        accept={accept}
        onChange={(e) => onFile(e.target.files?.[0] || null)}
      />
      <div className="muted" style={{ marginTop: 6 }}>
        Supported format: <b>.docx</b> only (format preservation).
      </div>
    </div>
  );
}
