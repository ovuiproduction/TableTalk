import React, { useEffect } from "react";
import "../css/chatbot.css";
import { useState, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function ChatBot() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState();
  const [data, setDate] = useState();
  const [fileName, setFileName] = useState();
  const [report, SetReport] = useState();
  const chatContainerRef = useRef(null);
  const chatHistoryRef = useRef([]);

  const handleQueryUpdate = (event) => {
    setQuery(event.target.value);
  };

  const handleQuerySubmit = async () => {
    if (!query) return;

    const formData = new FormData();
    formData.append("query", query);

    try {
      const response = await fetch("http://localhost:5000/process-query", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Network response was not ok.");
      const data = await response.json();
      const newMessage = { query, response: data.data };
      chatHistoryRef.current.push(newMessage);
      appendMessageToUI(newMessage);
      setQuery("");
    } catch (error) {
      console.error("Error fetching query response:", error);
    }
  };

  // Function to append new messages to the UI dynamically
  // const appendMessageToUI = (message) => {
  //   if (!chatContainerRef.current) return;

  //   const chatDiv = document.createElement("div");
  //   chatDiv.className = "chat-message";
  //   chatDiv.innerHTML = `
  //     <p className="user-query">${message.query}</p>
  //     <div class="chat-response">
  //       ${message.response
  //         .map(
  //           (row) =>
  //             `<div>${row.map((ele) => `<span>${ele}</span>`).join(" ")}</div>`
  //         )
  //         .join("")}
  //     </div>
  //     <hr/>
  //   `;

  //   chatContainerRef.current.appendChild(chatDiv);

  //   // Scroll to the latest message automatically
  //   chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
  // };

  const appendMessageToUI = (message) => {
    if (!chatContainerRef.current) return;

    const chatDiv = document.createElement("div");
    chatDiv.className = "chat-message";

    let tableHTML = `
      <table class="chat-table">
        <tbody>
          ${message.response
            .map(
              (row) =>
                `<tr scope="row">${row.map((ele) => `<td>${ele}</td>`).join("")}</tr>`
            )
            .join("")}
        </tbody>
      </table>
    `;

    chatDiv.innerHTML = `
      <p class="user-query">${message.query}</p>
      <div class="chat-response">
        ${tableHTML}
      </div>
      <hr class="separator" />
    `;

    chatContainerRef.current.appendChild(chatDiv);

    // Auto-scroll to the latest message
    chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
  };

  const handleFileChange = (event) => {
    const localfile = event.target.files[0];
    if (localfile) {
      console.log("File selected:", localfile.name);
      setFile(localfile);
    } else {
      console.log("No file selected");
      setFile(null);
    }
  };

  useEffect(() => {
    if (file) handleSubmit();
  }, [file]);

  const handleSubmit = async () => {
    if (file) {
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
        // const data = await response.json();
        setFileName(file.name);
        // console.log(data);
        // setDate(data);
        // navigate("/ResultsPage", { state: { results: data } });
      } catch (error) {
        console.error("Error uploading file:", error);
      } finally {
        // setIsLoading(false);
      }
    } else {
      console.log("No file selected for upload");
      //   setIsLoading(false);
    }
  };
  return (
    <>
      <div className="chatbot-container">
        <header className="chat-bot-header">
          <h1>TableTalk</h1>
        </header>
        <div className="chatbot-main">
          <div className="response-container">
            <p className="file-name">
              {fileName ? fileName : "WelCome To tables World"}
            </p>
            <div
              className="response-block"
              ref={chatContainerRef}
              style={{ maxHeight: "400px", overflowY: "auto" }}
            ></div>
          </div>
          <div className="input-block">
            <input type="file" accept="*" onChange={handleFileChange} />
            <input
              value={query}
              style={{ backgroundColor: file ? "white" : "#f0f0f0" }}
              placeholder={
                file
                  ? "Your data is ready. What insights are you looking for?"
                  : "Upload your file to proceed"
              }
              onChange={handleQueryUpdate}
              type="text"
            />
            <button onClick={handleQuerySubmit}>Submit</button>
          </div>
        </div>
      </div>
    </>
  );
}
