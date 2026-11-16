import { Link } from "react-router-dom";

function BookCard({ book }) {
  return (
    <Link className="book-card" to={`/books/${book.id}`}>
      <div className="book-cover">
        {book.photo_url ? (
          <img
            src={book.photo_url}
            alt={`Обложка книги «${book.title}»`}
          />
        ) : (
          <img
            src="/icons/book.svg"
            alt=""
            className="book-placeholder-icon"
          />
        )}
      </div>
      <div className="book-card-content">
        <h3>{book.title}</h3>
        <p className="book-card-meta">{book.author} · {book.genre}</p>
        <p className="book-card-summary">{book.summary}</p>
      </div>
      <div className="book-card-side">
        <span>{book.location}</span>
        <time dateTime={book.created_at}>{new Date(book.created_at).toLocaleDateString("ru-RU")}</time>
      </div>
    </Link>
  );
}

export default BookCard;
