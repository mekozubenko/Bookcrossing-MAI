import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  updateManagedListing,
  deleteManagedListing,
} from "../api";

function EditBook() {
  const { token } = useParams();

  const validToken = "test-secret-token";

  const [formData, setFormData] = useState({
    title: "Мастер и Маргарита",
    author: "Михаил Булгаков",
    genre: "Классика",
    summary: "Тестовое описание книги для редактирования.",
    location: "Корпус 3",
    contactValue: "@book_owner",
  });

  const [message, setMessage] = useState("");

  if (token !== validToken) {
    return (
      <main>
        <h1>Заявка не найдена</h1>
        <Link to="/">Вернуться на главную</Link>
      </main>
    );
  }

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  }

  async function handleSave(event) {
    event.preventDefault();

    try {
      await updateManagedListing(token, formData);
      setMessage("Изменения сохранены");
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function handleGiven() {
    try {
      await updateManagedListing(token, {
        status: "given",
      });

      setMessage("Книга отмечена как отданная");
    } catch (error) {
      setMessage(error.message);
    }
  }

  async function handleDelete() {
    const confirmed = window.confirm(
      "Вы уверены, что хотите удалить заявку?"
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteManagedListing(token);
      setMessage("Заявка удалена");
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <main>
      <h1>Редактирование заявки</h1>

      <form onSubmit={handleSave}>
        <div>
          <label htmlFor="title">Название книги</label>
          <input
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
          />
        </div>

        <div>
          <label htmlFor="author">Автор</label>
          <input
            id="author"
            name="author"
            value={formData.author}
            onChange={handleChange}
          />
        </div>

        <div>
          <label htmlFor="genre">Жанр</label>
          <select
            id="genre"
            name="genre"
            value={formData.genre}
            onChange={handleChange}
          >
            <option value="Классика">Классика</option>
            <option value="Фэнтези">Фэнтези</option>
            <option value="Антиутопия">Антиутопия</option>
            <option value="Научная литература">
              Научная литература
            </option>
          </select>
        </div>

        <div>
          <label htmlFor="summary">Описание</label>
          <textarea
            id="summary"
            name="summary"
            value={formData.summary}
            onChange={handleChange}
          />
        </div>

        <div>
          <label htmlFor="location">Место передачи</label>
          <select
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
          >
            <option value="Корпус 1">Корпус 1</option>
            <option value="Корпус 3">Корпус 3</option>
            <option value="Корпус 8">Корпус 8</option>
            <option value="Корпус 24">Корпус 24</option>
          </select>
        </div>

        <div>
          <label htmlFor="contactValue">Telegram</label>

          <input
            id="contactValue"
            name="contactValue"
            value={formData.contactValue}
            onChange={handleChange}
            placeholder="@username"
          />
        </div>

        <button type="submit">Сохранить</button>

        <button type="button" onClick={handleGiven}>
          Книгу отдали
        </button>

        <button type="button" onClick={handleDelete}>
          Удалить заявку
        </button>
      </form>

      {message && <p>{message}</p>}
    </main>
  );
}

export default EditBook;