import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null); // For modal
  const chatBoxRef = useRef(null);

  // Automatically scroll to the bottom when new messages are added
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (input.trim() === "") return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        user_input: input,
      });

      const data = response.data;

      if (data.images) {
        // Response includes breed, number, and images
        const botMessage = {
          role: "assistant",
          content: `Here are ${data.num} images of ${data.breed}:`,
          images: data.images,
        };
        setMessages((prev) => [...prev, botMessage]);
      } else {
        // Fallback to regular text response
        const botMessage = { role: "assistant", content: data };
        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = {
        role: "assistant",
        content: "Something went wrong! Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }

    setInput("");
  };

  const handleImageClick = (image) => {
    setSelectedImage(image); // Set the clicked image as the selected image
  };

  const closeModal = () => {
    setSelectedImage(null); // Close the modal
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <div ref={chatBoxRef} className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${
                msg.role === "user" ? "user-message" : "bot-message"
              }`}
            >
              <b>{msg.role === "user" ? "You" : "Bot"}:</b> {msg.content}
              {msg.images && (
                <div className="image-container">
                  {msg.images.map((img, i) => (
                    <img
                      key={i}
                      src={img.url}
                      alt={img.breeds?.[0]?.name || "Cat"}
                      className="cat-image"
                      onClick={() => handleImageClick(img)} // Handle click
                    />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Type your message..."
            className="chat-input"
          />
          <button onClick={sendMessage} className="send-button">
            Send
          </button>
        </div>
      </div>

      {selectedImage && (
        <div className="modal" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <img
              src={selectedImage.url}
              alt={selectedImage.breeds?.[0]?.name || "Cat"}
              className="modal-image"
            />
            {selectedImage.breeds && selectedImage.breeds.length > 0 && (
              <div className="modal-description">
                <h2>{selectedImage.breeds[0].name}</h2>
                <p>{selectedImage.breeds[0].description}</p>
                <p>
                  <b>Origin:</b> {selectedImage.breeds[0].origin}
                </p>
                <p>
                  <b>Temperament:</b> {selectedImage.breeds[0].temperament}
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
