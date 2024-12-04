document.getElementById("allergyForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const dishName = document.getElementById("dishName").value;
  const resultDiv = document.getElementById("result");
  const safeToEat = document.getElementById("safeToEat");

  const checkEgg = document.getElementById("checkEgg");
  const checkPotato = document.getElementById("checkPotato");
  const checkRawVegetable = document.getElementById("checkRawVegetable");
  const checkWhiteListDishes = document.getElementById("checkWhiteListDishes");
  const checkNuts = document.getElementById("checkNuts");
  const checkBurdock = document.getElementById("checkBurdock");
  const checkLotus = document.getElementById("checkLotus");
  const checkKonjac = document.getElementById("checkKonjac");
  const checkBuckwheat = document.getElementById("checkBuckwheat");

  const loadingSpinner = document.getElementById("loadingSpinner"); // スピナー要素
  const checkMark = document.getElementById("checkMark");
  const crossMark = document.getElementById("crossMark");



  // 初期化
  resultDiv.classList.remove("safe", "not-safe");
  resultDiv.querySelector("#safeToEat").textContent = "Checking...";
  checkEgg.textContent = "";
  checkPotato.textContent = "";
  checkRawVegetable.textContent = "";
  checkWhiteListDishes.textContent = "";
  checkNuts.textContent = "";
  checkBurdock.textContent = "";
  checkLotus.textContent = "";
  checkKonjac.textContent = "";
  checkBuckwheat.textContent = "";
  loadingSpinner.style.display = "block"; // スピナーを表示
  checkMark.style.display = "none"; // チェックマークを非表示
  crossMark.style.display = "none"; // クロスマークを非表示
  

  try {
      // サーバー送信イベント (SSE) を使って結果を逐次受信
      base_url = 'https://allergy-checker.onrender.com'; // or 'http://127.0.0.1:8000'
      base_url = 'http://127.0.0.1:8000'
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
          } else if (data.type === "nuts_tf") {
              checkNuts.textContent = `Nuts allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "burdock_tf") {
              checkBurdock.textContent = `Burdock allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "lotus_tf") {
              checkLotus.textContent = `Lotus allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "konjac_tf") {
              checkKonjac.textContent = `Konjac allergy check: ${data.result ? "Pass" : "Fail"}`;
          } else if (data.type === "buckwheat_tf") {
              checkBuckwheat.textContent = `Buckwheat allergy check: ${data.result ? "Pass" : "Fail"}`;    
          } else if (data.type === "white_list_tf") {
              checkWhiteListDishes.textContent = `White listed dish check: ${data.result ? "Pass" : "Fail"}`;   
          } else if (data.type === "safe_to_eat") {
              if (data.result) {
                resultDiv.querySelector("#safeToEat").textContent = "Safe to eat!";
                resultDiv.classList.add("safe");
                loadingSpinner.style.display = "none";
                checkMark.style.display = "block"; // チェックマークを表示
            } else {
                resultDiv.querySelector("#safeToEat").textContent = "Not safe to eat!";
                resultDiv.classList.add("not-safe");
                loadingSpinner.style.display = "none";
                crossMark.style.display = "block";
            }
            
            // 最後にイベントを閉じる
            eventSource.close();
          }
      };

      eventSource.onerror = function () {
          safeToEat.textContent = "Error occurred while checking. Please try again.";
          safeToEat.className = "not-safe";
          loadingSpinner.style.display = "none";
          crossMark.style.display = "none";
          eventSource.close();
      };
  } catch (error) {
      console.error(error);
      safeToEat.textContent = "Unexpected error occurred.";
      safeToEat.className = "not-safe";
      loadingSpinner.style.display = "none"; // スピナーを非表示
      crossMark.style.display = "none"; // チェックマークを非表示
  }
});
