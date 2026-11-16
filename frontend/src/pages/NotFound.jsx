import { Link } from "react-router-dom";

function NotFound() {
  return (
    <main>
      <h1>404 — Страница не найдена</h1>
      <Link to="/">Вернуться на главную</Link>
    </main>
  );
}

export default NotFound;