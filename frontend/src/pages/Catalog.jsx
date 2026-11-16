import { useState } from "react";

import BookCard from "../components/BookCard";
import listings from "../mocks/listings";

function Catalog() {
  const [search, setSearch] = useState("");
  const [genre, setGenre] = useState("");
  const [location, setLocation] = useState("");

  const filteredBooks = listings.filter((book) => {
    const query = search.trim().toLowerCase();

    const matchesSearch =
      book.title.toLowerCase().includes(query) ||
      book.author.toLowerCase().includes(query);

    const matchesGenre =
      !genre || book.genre === genre;

    const matchesLocation =
      !location || book.location === location;

    return matchesSearch && matchesGenre && matchesLocation;
  });

  return (
    <main className="catalog-page">
      <div className="catalog-controls">
        <div className="catalog-search">
          <input
            type="text"
            placeholder="Название или автор"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />

          <img src="/icons/search.svg" alt="" aria-hidden="true" />
        </div>

        <div className="catalog-filters">
          <select
            value={genre}
            onChange={(event) => setGenre(event.target.value)}
          >
            <option value="">Все жанры</option>
            <option value="Классика">Классика</option>
            <option value="Фэнтези">Фэнтези</option>
            <option value="Антиутопия">Антиутопия</option>
            <option value="Научная литература">
              Научная литература
            </option>
          </select>

          <select
            value={location}
            onChange={(event) => setLocation(event.target.value)}
          >
            <option value="">Все места</option>
            <option value="Корпус 1, вход">Корпус 1, вход</option>
            <option value="Корпус 3, холл">Корпус 3, холл</option>
            <option value="Корпус 8, холл">Корпус 8, холл</option>
            <option value="Корпус 24, вход">Корпус 24, вход</option>
          </select>

          <button
            className="catalog-reset"
            type="button"
            onClick={() => {
              setSearch("");
              setGenre("");
              setLocation("");
            }}
          >
            Сбросить
          </button>
        </div>
      </div>

      {filteredBooks.length === 0 ? (
        <p>По вашему запросу ничего не найдено.</p>
      ) : (
        <div className="book-list">
          {filteredBooks.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
      )}
    </main>
  );
}

export default Catalog;