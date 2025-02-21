import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Nav } from "../components/Nav";

export const Chat = () => {
  const [prompts, setPrompts] = useState([]); 
  const [userInput, setUserInput] = useState("");
  const navigate = useNavigate();

  const inputRef = useRef(null); 
  const messagesEndRef = useRef(null); 
  const [disabled, setDisabled] = useState(false);
  
  useEffect(() => {
    if (!localStorage.getItem("token")) {
      navigate("/");
    }
  }, []);

  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [prompts]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setDisabled(true)
    if (userInput.trim() === "") {
        setDisabled(false)
        return;
    }

    const userMessage = { role: "user", text: userInput };
    
    const botResponse = { role: "bot", text: `AI response to: ${userInput}` }; 

    setPrompts([...prompts, userMessage, botResponse]); 
    setUserInput(""); 

    inputRef.current.focus(); 
    setDisabled(false);
  };

  return (
    <div className="h-screen flex flex-col">
      <Nav text={""} />
      
      
      <div className="flex flex-col flex-grow p-5 bg-gray-100 overflow-y-auto">
        {prompts.length === 0 ? (
          <div className="text-center text-gray-500">Ask something...</div>
        ) : (
          prompts.map((msg, index) => (
            <div
              key={index}
              className={`p-3 rounded-lg mb-2 w-fit ${
                msg.role === "user" ? "bg-blue-500 text-white self-end" : "bg-gray-300 self-start"
              }`}
            >
              {msg.text}
            </div>
          ))
        )}
        <div ref={messagesEndRef} /> 
      </div>


      <form onSubmit={handleSubmit} className="flex items-center p-3 bg-white border-t">
        <input
          ref={inputRef}
          type="text"
          placeholder="Ask something..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          className="flex-grow p-2 border rounded-lg"
          
        />
        <button type="submit" disabled={disabled} className={disabled ?  "ml-2 px-4 py-2 bg-red-500 text-white rounded-lg" : "ml-2 px-4 py-2 bg-blue-500 text-white rounded-lg"}>
          Send
        </button>
      </form>
    </div>
  );
};
