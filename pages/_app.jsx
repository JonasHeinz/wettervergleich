import {
  Select,
  Typography,
  FormControl,
  InputLabel,
  MenuItem,
} from "@mui/material";
import "../App.css";
import Grid from "@mui/material/Grid2";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import dayjs from "dayjs";
import { useState } from "react";

export default function App() {
  const [parameter, setParameter] = useState("T");
  const [station, setStation] = useState("Zch_Rosengartenstrasse");
  const [date, setDate] = useState(dayjs("2022-04-17"));
  const [year, setYear] = useState(1992);
  const [interval, setInterval] = useState("woche");
  const years = [];
  for (let i = 1992; i <= 2024; i++) {
    years.push(i);
  }
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
              <FormControl fullWidth>
                <InputLabel id="parameter-lbl">Parameter</InputLabel>
                <Select
                  labelId="parameter-lbl"
                  label="Parameter"
                  value={parameter}
                  onChange={(e) => setParameter(e.target.value)}
                >
                  <MenuItem value="T">Temperatur</MenuItem>
                  <MenuItem value="RainDur">Niederschlagsdauer</MenuItem>
                  <MenuItem value="p">Luftdruck</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={8} />
            <Grid size={4}>
              <FormControl fullWidth>
                <InputLabel id="wetterstation-lbl">Wetterstation</InputLabel>
                <Select
                  labelId="wetterstation-lbl"
                  label="Wetterstation"
                  value={station}
                  onChange={(e) => setStation(e.target.value)}
                >
                  <MenuItem value="Zch_Stampfenbachstrasse">
                    Stampfenbachstrasse
                  </MenuItem>
                  <MenuItem value="Zch_Schimmelstrasse">
                    Schimmelstrasse
                  </MenuItem>
                  <MenuItem value="Zch_Rosengartenstrasse">
                    Rosengartenstrasse
                  </MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid size={8} />
            <Grid size={4}>
              <FormControl fullWidth>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                  <DatePicker
                    label="Start Datum"
                    value={date}
                    onChange={(newVal) => setDate(newVal)}
                  />
                </LocalizationProvider>
              </FormControl>
            </Grid>
            <Grid size={2}>
              <FormControl fullWidth>
                <InputLabel id="jahr-lbl">Vergleich mit Jahr</InputLabel>
                <Select
                  labelId="jahr-lbl"
                  label="Jahr"
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                >
                  {years.map((i) => (
                    <MenuItem value={i}>{i}</MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid size={4}>
              <FormControl fullWidth>
                <InputLabel id="intervall-lbl">Intervall</InputLabel>
                <Select
                  labelId="intervall-lbl"
                  label="Intervall"
                  value={interval}
                  onChange={(newVal) => setInterval(newVal)}
                >
                  <MenuItem value="woche">Woche</MenuItem>
                  <MenuItem value="monat">Monat </MenuItem>
                  <MenuItem value="jahr">Jahr</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </div>
      </div>
    </>
  );
}
