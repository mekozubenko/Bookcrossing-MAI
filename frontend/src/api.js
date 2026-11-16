const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getManagedListing(token) {
  const response = await fetch(`${API_URL}/api/manage/${token}`);

  if (!response.ok) {
    throw new Error("Не удалось загрузить заявку");
  }

  return response.json();
}

export async function updateManagedListing(token, data) {
  const response = await fetch(`${API_URL}/api/manage/${token}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error("Не удалось сохранить изменения");
  }

  return response.json();
}

export async function deleteManagedListing(token) {
  const response = await fetch(`${API_URL}/api/manage/${token}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Не удалось удалить заявку");
  }
}