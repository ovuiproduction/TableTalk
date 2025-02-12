// import React, { useState, useEffect } from "react";
// import "../css/chatbot.css";

// export default function TableTalk() {
//   const [file, setFile] = useState(null);
//   const [query, setQuery] = useState("");
//   const [fileName, setFileName] = useState("");
//   const [loader, setLoader] = useState(false);
//   const [response, setResponse] = useState("");
//   const [columns, setColumns] = useState();

//   const handleQuerySubmit = async () => {
//     if (!file) {
//       alert("File Is not Uploaded");
//       return;
//     }
//     if (!query) {
//       alert("Query is Empty!!!");
//       return;
//     }
//     setLoader(true);
//     try {
//       const response = await fetch("http://localhost:5000/process-query", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ query }),
//       });

//       if (!response.ok) {
//         throw new Error("Network response was not ok.");
//       }
//       setQuery("");
//       const data = await response.json();
//       console.log(data.data);
//       if (data.status === "ok") {
//         setResponse(data.data);
//       } else {
//         console.error("Error in fetching the file:", data);
//       }
//     } catch (error) {
//       console.error("Error fetching query response:", error);
//     } finally {
//       setLoader(false);
//     }
//   };

//   const handleFileChange = (event) => {
//     const selectedFile = event.target.files[0];
//     if (selectedFile) {
//       console.log("File selected:", selectedFile.name);
//       setFile(selectedFile);
//     } else {
//       console.log("No file selected");
//       setFile(null);
//     }
//   };

//   useEffect(() => {
//     if (file) handleSubmit();
//   }, [file]);

//   const handleSubmit = async () => {
//     if (!file) return;
//     const formData = new FormData();
//     formData.append("file", file);
//     try {
//       const response = await fetch("http://localhost:5000/process-file", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: formData,
//       });
//       const data = await response.json();
//       if (!response.ok) {
//         throw new Error("Network response was not ok.");
//       }
//       setColumns(data.tableData);
//       console.log(data.tableData);
//       setFileName(file.name);
//     } catch (error) {
//       console.error("Error uploading file:", error);
//     }
//   };

//   return (
//     <>
//       <div className="chatbot-container">
//         <header className="chat-bot-header">
//           <h1>
//             TableTalk <i> - Your Data, Your Language, Instant Insights!</i>
//           </h1>
//         </header>
//         <div className="chatbot-main">
//           <p className="file-name">
//             {fileName ? fileName : "Welcome To Tables World"}
//           </p>
//           <div className="input-block file-upload">
//             <label htmlFor="file">upload any csv,excel and sql file</label>
//             <input type="file" accept="*" onChange={handleFileChange} />
//           </div>
//           {columns && (
//             <div>
//               {columns.map((column) => (
//                 <span key={column}>{column}</span>
//               ))}
//             </div>
//           )}
//           <div className="query-block">
//             <input
//               type="text"
//               placeholder="Enter your query..."
//               value={query}
//               onChange={(e) => setQuery(e.target.value)}
//             />
//           </div>
//           <div className="input-block submit-btn">
//             <button onClick={handleQuerySubmit}>Submit</button>
//           </div>
//           {loader && <div className="loader"></div>}
//           {!loader && (
//             <>
//               {response && (
//                 <div className="chat-response">
//                   <p className="query">{response.query}</p>
//                   <p>
//                     {isNaN(response.ans)
//                       ? response
//                       : Number(response.ans).toFixed(2)}
//                   </p>
//                 </div>
//               )}
//             </>
//           )}
//         </div>
//       </div>
//     </>
//   );
// }

import React, { useState, useEffect } from "react";
import "../css/chatbot.css";

export default function TableTalk() {
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [fileName, setFileName] = useState("");
  const [loader, setLoader] = useState(false);
  const [response, setResponse] = useState("");
  const [columns, setColumns] = useState([]); // Fix: Initialize as empty array

  const handleQuerySubmit = async () => {
    if (!file) {
      alert("File Is not Uploaded");
      return;
    }
    if (!query) {
      alert("Query is Empty!!!");
      return;
    }
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
        setResponse(data.data); // Fix: Ensure correct data assignment
      } else {
        console.error("Error in fetching the query response:", data);
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
        body: formData, // Fix: No need to set Content-Type for FormData
      });

      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }

      const data = await response.json();
      setColumns(data.tableData);
      console.log(data);
      setFileName(file.name);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="chatbot-container">
      <header className="chat-bot-header">
        <h1>
          TableTalk <i>- Your Data, Your Language, Instant Insights!</i>
        </h1>
      </header>
      <div className="chatbot-main">
        <p className="file-name">{fileName || "Welcome To Tables World"}</p>
        <div className="input-block file-upload">
          <label htmlFor="file">Upload any CSV, Excel, or SQL file</label>
          <input type="file" accept="*" onChange={handleFileChange} />
        </div>
        {columns.length > 0 && (
          <>
            <p className="label-table-schema" htmlFor="file">
              Table Schema
            </p>
            <div className="table-info">
              {columns.map((column, index) => (
                <span key={index}>{column}</span>
              ))}
            </div>
          </>
        )}
        <div className="query-block">
          <input
            type="text"
            placeholder="Enter your query..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <div className="input-block submit-btn">
          <button onClick={handleQuerySubmit}>Submit</button>
        </div>
        {loader && <div className="loader"></div>}
        {!loader && response && (
          <div className="chat-response">
            <p className="query">{response.query}</p>
            <p>
              {Array.isArray(response.ans)
                ? response.ans.join(", ") // Join list elements with a comma
                : isNaN(response.ans)
                ? response.ans
                : Number(response.ans).toFixed(2)}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
