import { Link } from "react-router-dom";
import BookCard from "../components/BookCard";
import listings from "../mocks/listings";

function Home() {
  const latestBooks = [...listings]
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(0, 3);

  return (
    <main className="home-page">
      <section className="hero" aria-labelledby="hero-title">
        <h1 id="hero-title">Буккроссинг МАИ</h1>
        <p>Делитесь своими книгами<br />и находите новые</p>
        <div className="hero-actions">
          <Link className="button button-primary" to="/catalog">Найти книгу</Link>
          <Link className="button button-secondary" to="/give">Отдать книгу</Link>
        </div>
      </section>

      <section className="recent-section" aria-labelledby="recent-title">
        <div className="section-heading">
          <h2 id="recent-title">Свежие объявления</h2>
          <Link to="/catalog" className="section-more">Весь каталог →</Link>
        </div>
        <div className="book-list">
          {latestBooks.map((book) => <BookCard key={book.id} book={book} />)}
        </div>
      </section>

      <footer className="home-quote">
        <p>«Учитесь и читайте. Читайте книги серьёзные. Жизнь сделает остальное»</p>
        <span>— Ф. Достоевский</span>
      </footer>
    </main>
  );
}

export default Home;
