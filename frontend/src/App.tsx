import {
  HashRouter,
  Route,
  Routes,
} from "react-router-dom";
import Layout from "./pages/Layout/Layout";
import Chat from "./pages/Chat/Chat";




function App() {
  return (
    <>
      <HashRouter>
          <Routes>
              <Route path="/" element={<Layout />}>
                  <Route index element={<Chat/>} />
              </Route>
          </Routes>
      </HashRouter>
      </>
  );
}

export default App;
