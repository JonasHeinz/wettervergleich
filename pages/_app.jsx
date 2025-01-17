import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import "../App.css";

import { useState } from "react";
import { VegaViewer } from "./VegaViewer";
import { VegaForm } from "./VegaForm";
import { Header } from "./Header";
import { LinearProgress } from "@mui/material";
import Grid from "@mui/material/Grid2";

export default function App() {
  const [spec, setSpec] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const darkTheme = createTheme({
    palette: {
      mode: "dark",
    },
  });

  return (
    <>
      <div id="side">
        <ThemeProvider theme={darkTheme}>
          <CssBaseline />
          <Header />

          <div id="content">
            <Grid container spacing={2}>
              <Grid size={4}>
                <VegaForm
                  setSpec={setSpec}
                  spec={spec}
                  setIsLoading={setIsLoading}
                />
              </Grid>
              <Grid size={8}>
                {isLoading ? (
                  <LinearProgress />
                ) : (
                  <VegaViewer spec={spec.vis} />
                )}
              </Grid>
            </Grid>
          </div>
        </ThemeProvider>
      </div>
    </>
  );
}
