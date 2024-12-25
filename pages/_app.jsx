import { Typography } from "@mui/material";
import "../App.css";

import { useState } from "react";
import { VegaViewer } from "./VegaViewer";
import { VegaForm } from "./VegaForm";
import Grid from "@mui/material/Grid2";

export default function App() {
  const [spec, setSpec] = useState({});

  return (
    <>
      <div id="side">
        <div id="content">
          <header>
            <Typography variant="h3" component="h2">
              Wettervergleich
            </Typography>
          </header>
          <Grid container spacing={2}>
            <Grid size={4}>
              <VegaForm setSpec={setSpec} />
            </Grid>
            <Grid size={6}>
              <VegaViewer spec={spec} />
            </Grid>
          </Grid>
        </div>
      </div>
    </>
  );
}
