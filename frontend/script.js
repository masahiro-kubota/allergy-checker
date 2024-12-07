document.getElementById("allergyForm").addEventListener("submit", async function (event) {
  event.preventDefault();

  const dishName = document.getElementById("dishName").value;
  const resultDiv = document.getElementById("result");
  const safeToEat = document.getElementById("safeToEat");

  const checkEgg = document.getElementById("checkEgg");
  const checkPotato = document.getElementById("checkPotato");
  const checkRawVegetable = document.getElementById("checkRawVegetable");
  const checkNuts = document.getElementById("checkNuts");
  const checkBurdock = document.getElementById("checkBurdock");
  const checkLotus = document.getElementById("checkLotus");
  const checkKonjac = document.getElementById("checkKonjac");
  const checkBuckwheat = document.getElementById("checkBuckwheat");
  const checkCrustacean = document.getElementById("checkCrustacean");
  const checkBeef = document.getElementById("checkBeef");
  const checkRawFish = document.getElementById("checkRawFish");
  const checkPeach = document.getElementById("checkPeach");
  const checkPair = document.getElementById("checkPair");
  const checkMelon = document.getElementById("checkMelon");
  const checkWatermelon = document.getElementById("checkWatermelon");
  const checkCherry = document.getElementById("checkCherry");
  const checkMango = document.getElementById("checkMango");
  const checkBanana = document.getElementById("checkBanana");

  const loadingSpinner = document.getElementById("loadingSpinner"); // スピナー要素
  const questionMark = document.getElementById("questionMark");
  const checkMark = document.getElementById("checkMark");
  const crossMark = document.getElementById("crossMark");



  // 初期化
  resultDiv.classList.remove("safe", "not-safe");
  safeToEat.textContent = "Checking...";
  checkEgg.textContent = "";
  checkPotato.textContent = "";
  checkRawVegetable.textContent = "";
  checkNuts.textContent = "";
  checkBurdock.textContent = "";
  checkLotus.textContent = "";
  checkKonjac.textContent = "";
  checkBuckwheat.textContent = "";
  checkCrustacean.textContent = "";
  checkBeef.textContent = "";
  checkRawFish.textContent = "";
  checkPeach.textContent = "";
  checkPair.textContent = "";
  checkMelon.textContent = "";
  checkWatermelon.textContent = "";
  checkCherry.textContent = "";
  checkMango.textContent = "";
  checkBanana.textContent = "";



  loadingSpinner.style.display = "block"; // スピナーを表示
  questionMark.style.display = "none"; // チェックマークを非表示
  checkMark.style.display = "none"; // チェックマークを非表示
  crossMark.style.display = "none"; // クロスマークを非表示
  

  try {
      // サーバー送信イベント (SSE) を使って結果を逐次受信

      //base_url = 'https://allergy-checker.onrender.com'; // or 'http://127.0.0.1:8000'
      //base_url = 'http://127.0.0.1:8000'

      console.log("window.location.hostname: ", window.location.hostname);
      if (window.location.hostname === "0.0.0.0") {
        // ローカル環境の場合
        base_url = "http://localhost:8000";
        console.log("base_url: ", base_url);
    } else if (window.location.hostname === "allergy-checker.vercel.app") {
        // main環境の場合
        base_url = "https://allergy-checker.onrender.com";
        console.log("base_url: ", base_url);
    } else {
        // ローカルやその他の環境
        base_url = "https://allergy-checker-1.onrender.com";
        console.log("base_url: ", base_url);
    }
      const eventSource = new EventSource(`${base_url}/check_allergy_stream?dish_name=${encodeURIComponent(dishName)}`);

      eventSource.onmessage = function (event) {
          const data = JSON.parse(event.data);

          // フィールドごとに更新
          if (data.type === "egg_tf") {
              checkEgg.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "potato_tf") {
              checkPotato.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "raw_vegetables_tf") {
              checkRawVegetable.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "nuts_tf") {
              checkNuts.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "burdock_tf") {
              checkBurdock.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "lotus_tf") {
              checkLotus.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "konjac_tf") {
              checkKonjac.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "buckwheat_tf") {
              checkBuckwheat.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "crustacean_tf") {
              checkCrustacean.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "beef_tf") {
              checkBeef.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "raw_fish_tf") {
              checkRawFish.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "peach_tf") {
              checkPeach.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "pair_tf") {
              checkPair.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "melon_tf") {
              checkMelon.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "watermelon_tf") {
              checkWatermelon.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "cherry_tf") {
              checkCherry.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "mango_tf") {
              checkMango.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "banana_tf") {
              checkBanana.textContent = `${data.result ? "○" : "×"}`;
          } else if (data.type === "safe_to_eat") {
              if (data.result) {
                safeToEat.textContent = `${data.reason}`;;
                resultDiv.classList.add("safe");
                loadingSpinner.style.display = "none";
                checkMark.style.display = "block"; // チェックマークを表示
            } else {
                safeToEat.textContent = `${data.reason}`;;
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
          questionMark.style.display = "block";
          eventSource.close();
      };
  } catch (error) {
      console.error(error);
      safeToEat.textContent = "Unexpected error occurred.";
      safeToEat.className = "not-safe";
      loadingSpinner.style.display = "none"; // スピナーを非表示
      crossMark.style.display = "none"; // チェックマークを非表示
      questionMark.style.display = "block";
  }
});
