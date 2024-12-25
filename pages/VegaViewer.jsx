import { VegaLite } from "react-vega";
import { Box } from "@mui/material";
export function VegaViewer({ spec }) {
  return <Box sx={{ flex: 4 }}>{spec && <VegaLite spec={spec} />}</Box>;
}
