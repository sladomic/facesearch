import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

import AddPhotoAlternateOutlinedIcon from "@mui/icons-material/AddPhotoAlternateOutlined";
import { CircularProgressWithLabel } from "./CircularProgressWithLabel";

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
  const [loadingValue, setLoadingValue] = useState<number | undefined>();

  const onDrop = useCallback(
    async (acceptedFiles: (string | Blob)[]) => {
      let data = new FormData();
      data.append("uploadFile", acceptedFiles[0]);

      setLoadingValue(0);
      // https://javascript.info/fetch-progress
      // Step 1: start the fetch and obtain a reader
      let response = await fetch(`${apiUrl}:8000/search/`, {
        method: "PUT",
        body: data,
      });

      if (response.ok) {
        if (response.body) {
          const reader = response.body.getReader();

          // Step 2: get total length
          const contentLength = +(response.headers.get("Content-Length") ?? 0);

          // Step 3: read the data
          let receivedLength = 0; // received that many bytes at the moment
          let chunks = []; // array of received binary chunks (comprises the body)
          while (true) {
            const { done, value } = await reader.read();

            if (done) {
              break;
            }

            chunks.push(value);
            receivedLength += value.length;

            setLoadingValue((receivedLength / contentLength) * 100);
          }

          // Step 4: concatenate chunks into single Uint8Array
          let chunksAll = new Uint8Array(receivedLength); // (4.1)
          let position = 0;
          for (let chunk of chunks) {
            chunksAll.set(chunk, position); // (4.2)
            position += chunk.length;
          }

          // Step 5: decode into a string
          let result = new TextDecoder("utf-8").decode(chunksAll);

          // We're done!
          let resultDict = JSON.parse(result);
          setLoadingValue(undefined);
          setResults(resultDict);
        }
      } else {
        setLoadingValue(undefined);
        alert(response.body);
      }
    },
    [setResults]
  );
  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <div className="dropzone" {...getRootProps()}>
      <input {...getInputProps()} />
      {loadingValue || loadingValue === 0 ? (
        <>
          <p>Please wait…</p>
          <CircularProgressWithLabel
            color="inherit"
            variant="determinate"
            value={loadingValue}
          />{" "}
        </>
      ) : (
        <>
          <p>Drop an image of your face here</p>
          <AddPhotoAlternateOutlinedIcon />
        </>
      )}
    </div>
  );
}
