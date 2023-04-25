import { Button, Card, CardContent, Paper, Typography } from "@mui/material";
import ChatSideBar from "../../components/ChatSideBar/ChatSidebar";
import Divider from '@mui/material/Divider';
import { ChatEditor } from "../../components/ChatEditor/ChatEditor";
import { useState } from "react";
const Chat = () => {
  const [copywriteHTML, setCopywriteHTML] = useState<string>("");

  const handleEditorChange = (newData: string) => {
    setCopywriteHTML(newData);
  };

  return (
    <>
        <div className="flex">
          <div className="flex-grow flex w-2/3 mx-auto">
            <Paper className="flex flex-grow max-w-5xl mx-auto h-[calc(100vh-75px)]" elevation={1}>
              <ChatEditor data={copywriteHTML} onChange={handleEditorChange}/>
            </Paper>
          </div>
          <div className="w-1/3 max-w-sm">
            <ChatSideBar />
          </div>
        </div>
    </>
  );
};

export default Chat;
