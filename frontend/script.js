document.getElementById("allergyForm").addEventListener("submit", async function (event) {
  event.preventDefault(); // フォームのデフォルト送信を防止

  const dishName = document.getElementById("dishName").value;
  const resultDiv = document.getElementById("result");

  // 結果を初期化
  resultDiv.textContent = "Checking...";
  resultDiv.className = "";

  try {
      // Flaskエンドポイントにリクエストを送信
      base_url = 'https://allergy-checker.onrender.com'
    //base_url = 'http://127.0.0.1:8000'
      const response = await fetch(f"{base_url}/check_allergy", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ dish_name: dishName }),
      });

      if (!response.ok) {
          throw new Error("Failed to fetch result from server.");
      }

      const data = await response.json();

      // 結果を表示
      if (data.safe_to_eat) {
          resultDiv.textContent = "Safe to eat!";
          resultDiv.classList.add("safe");
      } else {
          resultDiv.textContent = "Not safe to eat!";
          resultDiv.classList.add("not-safe");
      }
  } catch (error) {
      console.error(error);
      resultDiv.textContent = "Error checking the dish. Please try again.";
      resultDiv.classList.add("not-safe");
  }
});
