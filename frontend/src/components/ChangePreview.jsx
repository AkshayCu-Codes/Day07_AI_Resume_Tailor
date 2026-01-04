import React from "react";

export default function ChangePreview({ changes = [] }) {
  if (!changes.length) return <div className="muted">No proposed changes to preview.</div>;

  return (
    <table className="table">
      <thead>
        <tr>
          <th>Section</th>
          <th>Before</th>
          <th>After</th>
          <th>Risk</th>
        </tr>
      </thead>
      <tbody>
        {changes.map((c, idx) => (
          <tr key={idx}>
            <td style={{ width: 110 }}><b>{c.section}</b></td>
            <td>{c.before}</td>
            <td>{c.after}</td>
            <td style={{ width: 70 }}>{c.risk}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
