import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

import AddPhotoAlternateOutlinedIcon from "@mui/icons-material/AddPhotoAlternateOutlined";
import { CircularProgress } from "@mui/material";

let apiUrl = "";
if (!process.env.NODE_ENV || process.env.NODE_ENV === "development") {
  apiUrl = "http://localhost";
} else {
  apiUrl = "http://ec2-18-222-149-34.us-east-2.compute.amazonaws.com";
}

export function Dropzone({
  setResults,
}: {
  setResults: React.Dispatch<React.SetStateAction<object | undefined>>;
}) {
  const [loading, setLoading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: (string | Blob)[]) => {
      let data = new FormData();
      data.append("uploadFile", acceptedFiles[0]);

      setLoading(true);
      const result = await fetch(`${apiUrl}:8000/search/`, {
        method: "PUT",
        body: data,
      });
      if (result.ok) {
        const resultDict = await result.json();
        setLoading(false);
        setResults(resultDict);
      } else {
        setLoading(false);
        alert(result.body);
      }
    },
    [setResults]
  );
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="dropzone" {...getRootProps()}>
      <input {...getInputProps()} />
      {loading ? (
        <CircularProgress color="inherit" />
      ) : (
        <>
          <p>Drop an image of your face here</p>
          <AddPhotoAlternateOutlinedIcon />
        </>
      )}
    </div>
  );
}
