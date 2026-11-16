import { useState } from "react";

function GiveBook() {
  const [formData, setFormData] = useState({
    title: "",
    author: "",
    genre: "",
    summary: "",
    location: "",
    contactValue: "",
    consent: false,
  });

  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [photo, setPhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState("");

  function handlePhotoChange(event) {
    const file = event.target.files?.[0];

    if (!file) return;

    setPhoto(null);
    setPhotoPreview("");

    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(file.type)) {
      setErrors((prev) => ({
        ...prev,
        photo: "Допустимы только JPG, PNG и WebP",
      }));
      event.target.value = "";
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setErrors((prev) => ({
        ...prev,
        photo: "Размер изображения не должен превышать 5 МБ",
      }));
      event.target.value = "";
      return;
    }

    setPhoto(file);

    const reader = new FileReader();

    reader.onload = () => {
      setPhotoPreview(reader.result);
    };

    reader.readAsDataURL(file);

    setErrors((prev) => ({
      ...prev,
      photo: "",
    }));
  }

  function handleChange(event) {
    const { name, value, type, checked } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  }

  function validateForm() {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = "Укажите название книги";
    }

    if (!formData.author.trim()) {
      newErrors.author = "Укажите автора";
    }

    if (!formData.genre) {
      newErrors.genre = "Выберите жанр";
    }

    if (formData.summary.trim().length < 20) {
      newErrors.summary = "Описание должно содержать минимум 20 символов";
    }

    if (!formData.location) {
      newErrors.location = "Выберите место передачи";
    }

    if (!formData.contactValue.trim()) {
      newErrors.contactValue = "Укажите Telegram";
    } else {
      const telegramRegex = /^@?[A-Za-z0-9_]{5,32}$/;

      if (!telegramRegex.test(formData.contactValue.trim())) {
        newErrors.contactValue =
          "Telegram-тэг должен содержать 5–32 символа: латиницу, цифры или _";
      }
    }

    if (!formData.consent) {
      newErrors.consent = "Необходимо согласие на обработку данных";
    }

    setErrors(newErrors);

    return Object.keys(newErrors).length === 0;
  }

  function handleSubmit(event) {
    event.preventDefault();

    const isValid = validateForm();

    if (!isValid) {
      return;
    }

    setIsSubmitting(true);

    setTimeout(() => {
      setIsSubmitting(false);
      setSubmitted(true);
    }, 500);
  }

  if (submitted) {
    return (
      <main>
        <h1>Заявка опубликована!</h1>

        <p>Сохраните секретную ссылку. Без неё заявку нельзя будет изменить.</p>

        <p>
          <strong>Секретная ссылка:</strong>
        </p>

        <code>http://localhost:5173/edit/test-secret-token</code>
      </main>
    );
  }

  return (
    <main>
      <h1>Отдать книгу</h1>

      <form className="listing-form" onSubmit={handleSubmit}>
        <div className="photo-field">
          <label htmlFor="photo">Обложка книги</label>

          <input
            id="photo"
            name="photo"
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handlePhotoChange}
            className="file-input-hidden"
          />

          <label htmlFor="photo" className="file-upload-area">
            <div className="file-upload-preview">
              {photoPreview ? (
                <img
                  src={photoPreview}
                  alt=""
                  className="file-upload-image"
                />
              ) : (
                <img
                  src="/icons/upload.svg"
                  alt=""
                  className="file-upload-icon"
                />
              )}
            </div>

            <div className="file-upload-text">
              <span className="file-upload-title">
                {photo ? photo.name : "Загрузить обложку"}
              </span>

              <span className="file-upload-hint">
                JPG, PNG или WebP · до 5 МБ
              </span>
            </div>
          </label>

          {errors.photo && (
            <p className="form-error">{errors.photo}</p>
          )}
        </div>

        <div>
          <label htmlFor="title">Название книги</label>

          <input
            id="title"
            name="title"
            type="text"
            value={formData.title}
            onChange={handleChange}
          />

          {errors.title && (
            <p className="form-error">{errors.title}</p>
          )}
        </div>

        <div>
          <label htmlFor="author">Автор</label>

          <input
            id="author"
            name="author"
            type="text"
            value={formData.author}
            onChange={handleChange}
          />

          {errors.author && <p>{errors.author}</p>}
        </div>

        <div>
          <label htmlFor="genre">Жанр</label>

          <select
            id="genre"
            name="genre"
            value={formData.genre}
            onChange={handleChange}
          >
            <option value="">Выберите жанр</option>
            <option value="Классика">Классика</option>
            <option value="Фэнтези">Фэнтези</option>
            <option value="Антиутопия">Антиутопия</option>
            <option value="Научная литература">Научная литература</option>
          </select>

          {errors.genre && <p>{errors.genre}</p>}
        </div>

        <div>
          <label htmlFor="summary">Описание</label>

          <textarea
            id="summary"
            name="summary"
            value={formData.summary}
            onChange={handleChange}
          />

          <p>{formData.summary.length} / 2000</p>

          {errors.summary && <p>{errors.summary}</p>}
        </div>

        <div>
          <label htmlFor="location">Место передачи</label>

          <select
            id="location"
            name="location"
            value={formData.location}
            onChange={handleChange}
          >
            <option value="">Выберите место</option>
            <option value="Корпус 1">Корпус 1</option>
            <option value="Корпус 3">Корпус 3</option>
            <option value="Корпус 8">Корпус 8</option>
            <option value="Корпус 24">Корпус 24</option>
          </select>

          {errors.location && <p>{errors.location}</p>}
        </div>

        <div>
          <label htmlFor="contactValue">Telegram-тэг</label>

          <input
            id="contactValue"
            name="contactValue"
            type="text"
            value={formData.contactValue}
            onChange={handleChange}
            placeholder="@username"
          />

          {errors.contactValue && <p>{errors.contactValue}</p>}
        </div>

        <div>
          <label>
            <input
              name="consent"
              type="checkbox"
              checked={formData.consent}
              onChange={handleChange}
            />

            Я согласен на обработку персональных данных
          </label>

          {errors.consent && <p>{errors.consent}</p>}
        </div>

        <button
          className="form-button"
          type="submit"
          disabled={isSubmitting}
        >
          {isSubmitting ? "Отправляем..." : "Опубликовать книгу"}
        </button>
      </form>
    </main>
  );
}

export default GiveBook;