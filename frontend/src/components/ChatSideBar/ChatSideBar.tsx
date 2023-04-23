import { useRef, useState, useEffect } from "react";
import { Box, IconButton, Paper, Typography } from "@mui/material";

import MessageInput from "../MessageInput/MessageInput";
import { ChatResponse, ChatMessage } from "../../api/model";
import ChatMessageBox from "../ChatMessageBox/ChatMessageBox";
import { useTheme } from "@mui/material/styles";
import { CleaningServices, ClearAll, ClearRounded } from "@mui/icons-material";

const ChatSideBar = () => {
  const theme = useTheme();
  const lastQuestionRef = useRef<ChatMessage>();
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<unknown>();
  const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);
  const [answers, setAnswers] = useState<ChatMessage[]>([]);

  useEffect(() => {
    const initialMessage: ChatMessage = {
      role: "Copilot",
      text: "你好，我是你的助手，有什么可以帮助你的吗？",
      time: new Date().toLocaleString(),
    };
    setAnswers([initialMessage]);
  }, []);

  const handleSendMessage = async (question: ChatMessage) => {
    lastQuestionRef.current = question;

    error && setError(undefined);
    setIsLoading(true);
    // setAnswers([...answers, question])
    const answerMessage: ChatResponse = {
      answer: {
        role: "Copilot",
        text:
          question.text +
          "的答案是<h1>Title</h1><h2>Sub title 1</h2><p>" +
          question.text +
          "</p>",
        time: new Date().toLocaleString(),
      },
      thoughts: "",
      data_points: [],
    };
    setAnswers([...answers, question, answerMessage.answer]);
    setIsLoading(false);
    // try {
    //     const response = await fetch("/chat", {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify({
    //         history: messages,
    //         newMessage: newMessage,
    //       }),
    //     });
    //     const data = await response.json();
    //     const answer = data.answer.text;
    //     const newAnswerMessage = {
    //       user: "Copilot",
    //       text: answer,
    //     };
    //     setMessages([...messages, newAnswerMessage]);
    //   } catch (error) {
    //     console.error(error);
    //   }
  };

  return (
    <Paper elevation={2} className="flex flex-col h-[calc(100vh-74px)]">
      <Box className="h-10 flex flex-row-reverse" sx={{backgroundColor: theme.palette.background}}>
        <IconButton>
          <CleaningServices sx={{fontSize:15}}/>
          <Typography sx={{fontSize:15}} variant="body1">清空</Typography>
        </IconButton>
      </Box>
      <Box className="flex flex-grow flex-col hover:overflow-y-auto overflow-hidden">
      
        {answers.map((answer, index) => (
          <>
            <Box
              key={index}
              sx={{
                display: "flex",
                flexDirection: "column",
              }}
            >
              <ChatMessageBox
                role={answer.role}
                text={answer.text}
                username={answer.role}
                timestamp={answer.time}
              />
            </Box>
          </>
        ))}
        <div ref={chatMessageStreamEnd} />
      </Box>
      <Box className="sticky mb-0">
        <MessageInput
          clearOnSend
          placeholder="请输入问题"
          disabled={isLoading}
          onSend={(question) => handleSendMessage(question)}
        />
      </Box>
    </Paper>
  );
};

export default ChatSideBar;
