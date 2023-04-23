import { useState } from "react";
import { InputBase, IconButton } from "@mui/material";
import { Mic as MicIcon, MicNone as MicNoneIcon } from "@mui/icons-material";
import SendIcon from "@mui/icons-material/Send";
import { ChatMessage } from "../../api/model";

interface IMessageProperties {
  disabled: boolean;
  placeholder?: string;
  clearOnSend?: boolean;
  onSend: (question: ChatMessage) => void;
}
const MessageInput = ({
  disabled,
  placeholder,
  clearOnSend,
  onSend,
}: IMessageProperties) => {
  const [isRecording, setIsRecording] = useState(false);
  const [userInput, setUserInput] = useState<string>("");

  const handleRecordStart = () => {
    setIsRecording(true);
  };

  const handleRecordStop = () => {
    setIsRecording(false);
  };

  const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
    if (ev.key === "Enter" && !ev.shiftKey) {
      ev.preventDefault();
      sendQuestion();
    }
  };

  const sendQuestion = () => {
    if (disabled || !userInput.trim()) {
      console.log("send disabled");
      console.log("question: " + userInput);
      return;
    }

    onSend({
      role: "User",
      text: userInput,
      time: new Date().toLocaleString()
    });

    if (clearOnSend) {
      setUserInput("");
    }
  };


  const onQuestionChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    setUserInput(ev.target.value);
    };

  return (
    <div className="flex flex-grow border border-solid border-gray-400 ">
      {isRecording ? (
        <IconButton color="primary" onMouseUp={handleRecordStop}>
          <MicNoneIcon />
        </IconButton>
      ) : (
        <IconButton color="primary" onMouseDown={handleRecordStart}>
          <MicIcon />
        </IconButton>
      )}
      <InputBase
        placeholder={placeholder}
        value={userInput}
        onKeyDown={onEnterPress}
        onChange={onQuestionChange}
        className="flex flex-grow"
      />
      <IconButton
        color="primary"
        onClick={sendQuestion}
      >
        <SendIcon />
      </IconButton>
    </div>
  );
};

export default MessageInput;
