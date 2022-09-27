import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

import AddPhotoAlternateOutlinedIcon from "@mui/icons-material/AddPhotoAlternateOutlined";
import { CircularProgress, ImageList, ImageListItem } from "@mui/material";

export function Dropzone() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<string[]>();

  const onDrop = useCallback(async (acceptedFiles: (string | Blob)[]) => {
    let data = new FormData();
    data.append("uploadFile", acceptedFiles[0]);

    setLoading(true);
    const result = await fetch("http://localhost:8000/search/", {
      method: "PUT",
      body: data,
    });
    setLoading(false);
    if (result.ok) {
      const resultList: string[] = await result.json();
      setResults(resultList);
    } else {
      alert(result.body);
    }
  }, []);
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return results ? (
    <ImageList>
      {results.map((result) => (
        <ImageListItem key={result}>
          <img src={result} alt={result} loading="lazy" />
        </ImageListItem>
      ))}
    </ImageList>
  ) : (
    <div className="dropzone" {...getRootProps()}>
      <input {...getInputProps()} />
      {loading ? <CircularProgress /> : <AddPhotoAlternateOutlinedIcon />}
    </div>
  );
}
