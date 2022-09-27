import { ImageList, ImageListItem } from "@mui/material";
import React, { useState } from "react";
import "./App.css";
import { Dropzone } from "./Dropzone";

function App() {
  const [results, setResults] = useState<Object>();

  return (
    <div className="app">
      {results ? (
        <ImageList>
          {Object.entries(results).map(([key, value]) => (
            <ImageListItem key={key}>
              <img src={`data:image/jpeg;base64,${value}`} alt={key} />
              <a
                className="download"
                href={`data:image/jpeg;base64,${value}`}
                download={key}
              >
                <p>Download</p>
              </a>
            </ImageListItem>
          ))}
        </ImageList>
      ) : (
        <Dropzone setResults={setResults} />
      )}
    </div>
  );
}

export default App;
