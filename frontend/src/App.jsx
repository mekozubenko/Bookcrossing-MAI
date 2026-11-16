import { BrowserRouter, Routes, Route } from "react-router-dom";

import Header from "./components/Header";

import Home from "./pages/Home";
import Catalog from "./pages/Catalog";
import Book from "./pages/Book";
import GiveBook from "./pages/GiveBook";
import EditBook from "./pages/EditBook";
import Privacy from "./pages/Privacy";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <Header />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/catalog" element={<Catalog />} />
        <Route path="/books/:id" element={<Book />} />
        <Route path="/give" element={<GiveBook />} />
        <Route path="/edit/:token" element={<EditBook />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;