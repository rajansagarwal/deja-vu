import React from "react";

const ChatPage = () => {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
      <div style={{ flex: 1 }}></div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "50px",
          margin: "0 auto",
          marginBottom: "40px",
          cursor: "default",
        }}
      >
        <input
          type="text"
          placeholder="Question"
          style={{
            height: "30px",
            width: "500px",
            border: "1px solid gray",
            borderRadius: "5px",
            textAlign: "left",
            paddingLeft: "10px", 
            margin: "0 auto",
            marginBottom: "20px",
            cursor: "default",
          }}
        />
      </div>
    </div>
  );
};

export default ChatPage;
