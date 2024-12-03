document.getElementById("allergyForm").addEventListener("submit", async function (event) {
  event.preventDefault(); // フォームのデフォルト送信を防止

  const dishName = document.getElementById("dishName").value;
  const resultDiv = document.getElementById("result");
  const safeToEat = document.getElementById("safeToEat");
  const checkEgg = document.getElementById("checkEgg");
  const checkPotato = document.getElementById("checkPotato");
  const checkRawVegetable = document.getElementById("checkRawVegetable");
  const checkWhiteListDishes = document.getElementById("checkWhiteListDishes");


  // 結果を初期化
  resultDiv.querySelector("#safeToEat").textContent = "Checking...";
  checkEgg.textContent = "";
  checkPotato.textContent = "";
  checkRawVegetable.textContent = "";
  checkWhiteListDishes.textContent = "";

  try {
      // Flaskエンドポイントにリクエストを送信
      base_url = 'https://allergy-checker.onrender.com'
      base_url = 'http://127.0.0.1:8000'
      const response = await fetch(`${base_url}/check_allergy`, {
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
      checkEgg.textContent = `Egg allergy check: ${data.check_egg ? "Pass" : "Fail"}`;
      checkPotato.textContent = `Potato allergy check: ${data.check_potato ? "Pass" : "Fail"}`;
      checkRawVegetable.textContent = `Raw vegetable allergy check: ${data.check_raw_vegetable ? "Pass" : "Fail"}`;
      checkWhiteListDishes.textContent = `White listed dish check: ${data.check_white_list_dishes ? "Pass" : "Fail"}`;

      // 結果を表示
      if (data.safe_to_eat) {
          resultDiv.querySelector("#safeToEat").textContent = "Safe to eat!";
          resultDiv.classList.add("safe");
      } else {
          resultDiv.querySelector("#safeToEat").textContent = "Not safe to eat!";
          resultDiv.classList.add("not-safe");
      }
  } catch (error) {
      console.error(error);
      resultDiv.textContent = "Error checking the dish. Please try again.";
      resultDiv.classList.add("not-safe");
  }
});
