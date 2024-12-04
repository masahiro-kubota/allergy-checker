document.getElementById("allergyForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const dishName = document.getElementById("dishName").value;
  const resultDiv = document.getElementById("result");
  const safeToEat = document.getElementById("safeToEat");
  const checkEgg = document.getElementById("checkEgg");
  const checkPotato = document.getElementById("checkPotato");
  const checkRawVegetable = document.getElementById("checkRawVegetable");
  const checkWhiteListDishes = document.getElementById("checkWhiteListDishes");

  // 初期化
  resultDiv.querySelector("#safeToEat").textContent = "Checking...";
  checkEgg.textContent = "";
  checkPotato.textContent = "";
  checkRawVegetable.textContent = "";
  checkWhiteListDishes.textContent = "";

  try {
      // サーバー送信イベント (SSE) を使って結果を逐次受信
      base_url = 'https://allergy-checker.onrender.com'; // or 'http://127.0.0.1:8000'
      //base_url = 'http://127.0.0.1:8000'
      const eventSource = new EventSource(`${base_url}/check_allergy_stream?dish_name=${encodeURIComponent(dishName)}`);

      eventSource.onmessage = function (event) {
          const data = JSON.parse(event.data);

          // フィールドごとに更新
          if (data.type === "egg_tf") {
              checkEgg.textContent = `Egg allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "potato_tf") {
              checkPotato.textContent = `Potato allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "raw_vegetables_tf") {
              checkRawVegetable.textContent = `Raw vegetable allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "white_list_tf") {
              checkWhiteListDishes.textContent = `White listed dish check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "safe_to_eat") {
              if (data.result) {
                resultDiv.querySelector("#safeToEat").textContent = "Safe to eat!";
                resultDiv.classList.add("safe");
            } else {
                resultDiv.querySelector("#safeToEat").textContent = "Not safe to eat!";
                resultDiv.classList.add("not-safe");

              // 最後にイベントを閉じる
              eventSource.close();
            }
          }
      };

      eventSource.onerror = function () {
          safeToEat.textContent = "Error occurred while checking. Please try again.";
          safeToEat.className = "not-safe";
          eventSource.close();
      };
  } catch (error) {
      console.error(error);
      safeToEat.textContent = "Unexpected error occurred.";
      safeToEat.className = "not-safe";
  }
});
