import React from "react";

export default function StyleSelector({ style, setStyle, strictness, setStrictness }) {
  return (
    <div>
      <label>Writing Style</label>
      <select value={style} onChange={(e) => setStyle(e.target.value)}>
        <option>Professional</option>
        <option>Concise</option>
        <option>Impact-Oriented</option>
        <option>Technical</option>
        <option>Executive</option>
      </select>

      <div style={{ marginTop: 10 }}>
        <label>Accuracy Mode</label>
        <select value={strictness} onChange={(e) => setStrictness(e.target.value)}>
          <option>Strict</option>
          <option>Assisted</option>
        </select>
        <div className="muted" style={{ marginTop: 6 }}>
          <b>Strict</b> blocks tailoring if missing evidence is detected. <b>Assisted</b> allows tailoring while still showing questions.
        </div>
      </div>
    </div>
  );
}
