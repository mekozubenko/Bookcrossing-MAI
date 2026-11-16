import { Link, NavLink } from "react-router-dom";

function Header() {
  return (
    <header className="site-header">
      <Link className="site-brand" to="/">Буккроссинг МАИ</Link>
      <nav className="site-nav" aria-label="Главное меню">
        <NavLink className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`} to="/catalog">Найти книгу</NavLink>
        <NavLink className={({ isActive }) => `nav-link ${isActive ? "nav-link-active" : ""}`} to="/give">Отдать книгу</NavLink>
      </nav>
    </header>
  );
}

export default Header;
