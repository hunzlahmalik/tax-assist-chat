"use client";

import Menu from "@/components/Menu";
import { Send } from "lucide-react"; // Importing the Send icon from lucide-react
import Message, { Skeleton } from "@/components/Message";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/components/ui/use-toast";
import { useEffect, useRef, useState } from "react";
import { v4 as idGen } from "uuid";
import { withAuth } from "@/components/WithAuth";
import { Upload } from "lucide-react";
import { httpRequest } from "@/mylib/interceptor";
import { AxiosResponse } from "axios";

type Message = {
  id: string;
  message: string;
  file?: string | object | File;
  timestamp?: string;
  isUser: boolean;
  isNew?: boolean;
};

function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const { toast } = useToast();
  const ws = useRef<WebSocket | null>(null);
  const token = localStorage.getItem("accessToken");

  const urlParams = new URLSearchParams(window.location.search);
  let chat_id = urlParams.get("id") || "new";

  // handle chat_id undefined
  if (chat_id === undefined) {
    chat_id = "new";
  }

  const wsurl = `ws://${process.env.NEXT_PUBLIC_BACKEND_DOMAIN?.replace(
    "http://",
    ""
  ).replace("https://", "")}/ws/chat/${chat_id}/?token=${token}`;

  const get_messages_url = `/api/chat/${chat_id}/messages/`;

  useEffect(() => {
    // Connect to websocket server
    ws.current = new WebSocket(wsurl);

    ws.current.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.current.onmessage = (event) => {
      const messageData = JSON.parse(event.data);
      setMessages((prev) => [
        ...prev,
        {
          id: messageData.uuid,
          message: messageData.content,
          file: messageData.file,
          timestamp: messageData.timestamp,
          isUser: false,
          isNew: true,
        },
      ]);
      setLoading(false);
    };

    ws.current.onclose = () => {
      console.log("WebSocket disconnected");
      toast({
        title: "WebSocket disconnected",
        description: "WebSocket connection was closed",
      });
    };

    return () => {
      // Cleanup websocket connection
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  useEffect(() => {
    // Fetch previous messages when the component mounts
    if (chat_id === "new") {
      return;
    }
    httpRequest
      .get(get_messages_url) // Make a GET request to fetch previous messages
      .then((response: AxiosResponse<any>) => {
        // Set the retrieved messages in the state
        // add key isUser in the response
        response.data.results.reverse().forEach((message: any) => {
          message.isUser = message.user && message.user.username === "llm";
          message.message = message.content;
        });
        setMessages(response.data.results as unknown as Message[]);
      })
      .catch((error) => {
        // Handle errors if any
        console.error("Error fetching previous messages:", error);
        toast({
          title: "Error fetching messages",
          description: "An error occurred while fetching previous messages",
        });
      });
  }, [chat_id]);

  function handleEmit() {
    setLoading(true);
    if (message.trim() !== "") {
      setMessages((prev) => [...prev, { id: idGen(), isUser: true, message }]);
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ message: message }));
      }
      setMessage("");
    }
  }

  function handleFileUpload(file: File) {
    setLoading(true);
    const reader = new FileReader();
    reader.onloadend = () => {
      const fileData = {
        name: file.name,
        mime: file.type,
        data:
          typeof reader.result === "string" ? reader.result.split(",")[1] : "", // Add null check before accessing result
      };
      console.log(fileData);
      setMessages((prev) => [
        ...prev,
        {
          id: idGen(),
          isUser: true,
          file: {
            name: file.name,
            type: file.type,
            data: (reader.result as string)?.split(",")[1], // Extracting base64 data
          },
          message: "Uploaded a file",
        },
      ]);
      if (ws.current && ws.current.readyState === WebSocket.OPEN) {
        ws.current.send(JSON.stringify({ message: "", file: fileData }));
      }
    };
    reader.readAsDataURL(file);
  }

  function handleFileInputChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    console.log(file);
    if (file) {
      handleFileUpload(file);
    }
  }

  function clear() {
    setMessages([]);
  }

  function updateScroll() {
    var element = scrollRef.current;
    if (!element) return;
    element.scrollTop = element.scrollHeight;
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(updateScroll, [messages]);

  return (
    <div>
      <Menu clear={clear} />
      <div className="input w-full flex flex-col justify-between h-screen">
        <div
          className="messages w-full mx-auto h-full mb-4 overflow-auto flex flex-col gap-10 pt-10 max-[900px]:pt-20 scroll-smooth"
          ref={scrollRef}
        >
          {messages.map((message) => (
            <Message
              key={message.id}
              id={message.id}
              isUser={message.isUser}
              message={message.message}
              isNew={message.isNew ?? false}
              file={message.file as unknown as File} // Update the type of the file prop
            />
          ))}
          {loading && <Skeleton />}
        </div>
        <div className="w-[40%] max-[900px]:w-[90%] flex flex-row gap-3 mx-auto mt-auto">
          <Input
            onKeyDown={(e) => {
              if (e.keyCode === 13 && message) {
                handleEmit();
              }
            }}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Send a message"
            className="h-12"
          />
          {/* Button to open file upload */}
          <Button className="h-12 font-semibold">
            <label htmlFor="file-upload-input">
              <Upload size={16} /> {/* Using the Upload icon */}
            </label>
          </Button>
          <input
            type="file"
            onChange={handleFileInputChange}
            accept=".pdf,.jpg,.jpeg,.png"
            className="hidden"
            name="file-upload-input"
            id="file-upload-input"
          />
          {/* Button to send message */}
          <Button
            disabled={!message}
            onClick={handleEmit}
            className="h-12 font-semibold"
          >
            Send
          </Button>
        </div>
        <span className="mx-auto mb-6 text-xs mt-3 text-center">
          ChatGPT may produce inaccurate information about people, places, or
          facts.
        </span>
      </div>
    </div>
  );
}

export default withAuth(Chat);
