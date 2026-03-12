import { useEffect, useState } from "react";
import API from "./api";
import "./App.css";

function Dashboard({ token }) {
  const [students, setStudents] = useState([]);
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [screenshot, setScreenshot] = useState(null); // NEW

  useEffect(() => {
    const getStudents = async () => {
      const res = await API.get("/students", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setStudents(res.data);
    };

    getStudents();
  }, [token]);

  const capturePage = async () => {
    try {
      new URL(url);
    } catch {
      alert("Please enter a valid URL");
      return;
    }

    try {
      setLoading(true);

      const res = await API.get(`/screenshot?url=${encodeURIComponent(url)}`);

      const image = res.data.image;

      setScreenshot(`data:image/png;base64,${image}`); // store screenshot

    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") capturePage();
  };

  return (
    <div className="dashboard-container">

      {/* URL SEARCH BAR */}

      <div className="capture-box">
        <input
          type="text"
          placeholder="Enter URL (example: https://news.ycombinator.com)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button onClick={capturePage} disabled={loading}>
          {loading ? "Capturing..." : "Capture Page"}
        </button>
      </div>

      {loading && <p className="loading-text">Capturing screenshot...</p>}

      {/* SCREENSHOT PREVIEW */}

      {screenshot && (
        <div className="preview-container">
          <h3>Page Preview</h3>

          <div className="preview-window">
            <img src={screenshot} alt="Captured page" />
          </div>
        </div>
      )}

      {/* STUDENTS LIST */}

      <h2>Students</h2>

      <div className="students-grid">
        {students.map((s) => (
          <div className="student-card" key={s._id}>
            <strong>{s.name}</strong>
            <br />
            Course: {s.course}
          </div>
        ))}
      </div>

    </div>
  );
}

export default Dashboard;