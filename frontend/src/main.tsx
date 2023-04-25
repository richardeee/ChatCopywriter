import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";
import { CssBaseline, useMediaQuery } from "@mui/material";
import {
  createTheme,
  StyledEngineProvider,
  ThemeProvider,
} from "@mui/material/styles";
import "./index.css";

const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement!);
export const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

const Main = () => {
  const [mode, setMode] = React.useState<'light' | 'dark'>('light');
  

  const theme = React.useMemo(
    () =>
      createTheme({
        components: {
          MuiPopover: {
            defaultProps: {
              container: rootElement,
            },
          },
          MuiPopper: {
            defaultProps: {
              container: rootElement,
            },
          },
        },
        palette: {
          mode: mode,
          primary: {
            main: "#673ab7",
          },
          secondary: {
            main: "#f50057",
          },
        },
      }),
    [mode],
  );

  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  return (
    <React.StrictMode>
      <StyledEngineProvider injectFirst>
      <ColorModeContext.Provider value={colorMode}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <App />
        </ThemeProvider>
        </ColorModeContext.Provider>
      </StyledEngineProvider>
    </React.StrictMode>
  );
};

root.render(<Main />);
