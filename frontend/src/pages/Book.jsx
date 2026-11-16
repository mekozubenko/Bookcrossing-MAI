import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import listings from "../mocks/listings";

function Book() {
  const { id } = useParams();

  const [showContact, setShowContact] = useState(false);
  const [copied, setCopied] = useState(false);

  const book = listings.find((item) => item.id === Number(id));

  if (!book) {
    return (
      <main>
        <h1>Книга не найдена</h1>
        <Link to="/catalog">Вернуться в каталог</Link>
      </main>
    );
  }

  function handleToggleContact() {
    setShowContact((prev) => !prev);
    setCopied(false);
  }

  function handleCopy() {
    navigator.clipboard.writeText(book.contact_value);
    setCopied(true);
  }

  return (
    <main>
      <div className="book-detail">
        <div className="book-detail-cover">
          {book.photo_url ? (
            <img
              src={book.photo_url}
              alt={`Обложка книги ${book.title}`}
            />
          ) : (
            <img
              src="/icons/book.svg"
              alt=""
              className="book-placeholder-icon"
            />
          )}
        </div>

        <div className="book-detail-info">
          <h1>{book.title}</h1>

          <p>Автор: {book.author}</p>
          <p>Жанр: {book.genre}</p>
          <p>{book.summary}</p>
          <p>
            <strong>Дата публикации:</strong>{" "}
            {new Date(book.created_at).toLocaleDateString("ru-RU")}
          </p>

          <div className="book-detail-bottom">
            <p>Место передачи: {book.location}</p>

            <button
              type="button"
              className="book-contact-button"
              onClick={handleToggleContact}
            >
              {showContact ? "Скрыть контакт" : "Показать контакт"}
            </button>

            {showContact && (
              <div>
                <p>
                  <strong>Контакт:</strong> {book.contact_value}
                </p>

                <button
                  type="button"
                  className="book-copy-button"
                  onClick={handleCopy}
                >
                  {copied ? "Скопировано!" : "Скопировать"}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

export default Book;