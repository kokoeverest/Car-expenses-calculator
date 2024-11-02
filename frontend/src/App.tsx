import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import WelcomePage from "./pages/WelcomePage";
import "./App.css";
import { Box } from "@mui/material";
import Header from "./components/Header";
import CarDetailsForm from "./features/CarDetailsForm";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();
const App: React.FC = () =>
{
  return (
    
    <QueryClientProvider client= {queryClient}>
      <Router>
        <Header />
        <Box className="main-content">
          <Routes>
            <Route path="/" element={ <WelcomePage /> } />
            <Route path="/form" element={ < CarDetailsForm/> } />

            
          </Routes>
        </Box>
      </Router>

    </QueryClientProvider>
  );
};

export default App;
