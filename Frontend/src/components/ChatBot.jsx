import React, { useState, useEffect } from "react";
import "../css/chatbot.css";

export default function ChatBot() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [fileName, setFileName] = useState("");
  const [loader, setLoader] = useState(false);
  const [loadereval,setLoaderEval] = useState(false);
  const [download_url, setUrl] = useState("");
  const [result, setResult] = useState("");

  const handleQuerySubmit = async () => {
    setLoader(true);
    try {
      const response = await fetch("http://localhost:5000/process-query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      const data = await response.json();
      if (data.status === "ok") {
        setUrl(data.url);
      } else {
        console.error("Error in fetching the file:", data);
      }
    } catch (error) {
      console.error("Error fetching query response:", error);
    } finally {
      setLoader(false);
    }
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile) {
      console.log("File selected:", selectedFile.name);
      setFile(selectedFile);
    } else {
      console.log("No file selected");
      setFile(null);
    }
  };

  useEffect(() => {
    if (file) handleSubmit();
  }, [file]);

  const handleSubmit = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await fetch("http://localhost:5000/process-file", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      setFileName(file.name);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  const handleEvalute = async () => {
    setLoaderEval(true);
    try {
      const response = await fetch("http://localhost:5000/evalute-file", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }
      const data = await response.json();
      if(data.status === "ok"){
        setResult(data.score);
        setLoaderEval(false);
      }
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <>
      <div className="chatbot-container">
        <header className="chat-bot-header">
          <h1>TableTalk</h1>
        </header>
        <div className="chatbot-main">
          <p className="file-name">
            {fileName ? fileName : "Welcome To Tables World"}
          </p>
          <div className="input-block">
            <input type="file" accept="*" onChange={handleFileChange} />
            <button onClick={handleQuerySubmit}>Submit</button>
          </div>
          <div className="response">
            {loader && <div className="loader"></div>}
            {download_url && (
              <>
                <a href={download_url} download>
                  Download Processed File
                </a>
                <button className="evalute-btn" onClick={handleEvalute}>
                  Evalute
                </button>
              </>
            )}
            {loadereval && <div className="loader"></div>}
            {result && (
              <div className="evaluation-score-board">
                <h2>Evaluation Scores</h2>
                <p>
                  <strong>Table Score:</strong> {result.table_score}
                </p>
                <p>
                  <strong>Generated Response Score:</strong> {result.res_score}
                </p>
                <p>
                  <strong>Total Score:</strong> {result.total_score}
                </p>
                <p>
                  <strong>Final Weighted Score:</strong> {result.f_score}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}