import {
  AccountCircleRounded,
  MoreVert,
  Reddit,
  ThumbDown,
  ThumbUp,
} from "@mui/icons-material";
import { styled } from "@mui/material/styles";
import {
  Avatar,
  Box,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Divider,
  IconButton,
  Stack,
  Typography,
  Badge,
} from "@mui/material";

interface IChatMessageProps {
  role: string;
  text: string;
  username?: string;
  avatar?: string;
  timestamp?: string;
}
const StyledBadge = styled(Badge)(({ theme }) => ({
  "& .MuiBadge-badge": {
    backgroundColor: "#44b700",
    color: "#44b700",
    boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
    "&::after": {
      position: "absolute",
      top: 0,
      left: 0,
      width: "100%",
      height: "100%",
      borderRadius: "50%",
      animation: "ripple 1.2s infinite ease-in-out",
      border: "1px solid currentColor",
      content: '""',
    },
  },
  "@keyframes ripple": {
    "0%": {
      transform: "scale(.8)",
      opacity: 1,
    },
    "100%": {
      transform: "scale(2.4)",
      opacity: 0,
    },
  },
}));

const ChatMessageBox = ({
  role,
  text,
  username = "User",
  avatar = "",
  timestamp = "",
}: IChatMessageProps) => {
  const isAssistant = role != "User";
  const messageText = isAssistant ? (
    <Typography
      component="div"
      sx={{fontSize: 15}}
      dangerouslySetInnerHTML={{
        __html: text,
      }}
    />
  ) : (
    <Typography sx={{fontSize: 15}} color="textPrimary">{text}</Typography>
  );

  return (
    <>
      <Card className="m-1">
        <CardHeader
          avatar={
            isAssistant ? (
              <StyledBadge
                overlap="circular"
                anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
                variant="dot"
              >
                <Avatar className="bg-yellow-500">C</Avatar>
              </StyledBadge>
            ) : (
              <StyledBadge
                overlap="circular"
                anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
                variant="dot"
              >
                <Avatar className="bg-blue-500">
                  <AccountCircleRounded />{" "}
                </Avatar>
              </StyledBadge>
            )
          }
          action={
            <IconButton>
              <MoreVert />
            </IconButton>
          }
          title={username}
          subheader={timestamp}
        />
        <CardContent>
          {messageText}
        </CardContent>
        <CardActions disableSpacing>
          {isAssistant && (
            <>
              <IconButton>
                <ThumbUp sx={{ fontSize: 15 }} />
              </IconButton>
              <IconButton>
                <ThumbDown sx={{ fontSize: 15 }} />
              </IconButton>
            </>
          )}
        </CardActions>
      </Card>
    </>
  );
};

export default ChatMessageBox;
