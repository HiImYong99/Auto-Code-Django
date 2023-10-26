// 요청 답변 기록js
const $remove_btn = document.querySelector("#history-remove");
const $question = document.querySelector("#question");
const $result = document.querySelector("#result");

// 유저의 요청사항 및 ai의 결과 내용 불러오기
function load_history() {
  let ai = localStorage.getItem("ai")
    ? JSON.parse(localStorage.getItem("ai"))
    : [];
  let detail = localStorage.getItem("detail")
    ? JSON.parse(localStorage.getItem("detail"))
    : [];
  if (ai.length === 0) {
    $question.innerText = "사용자가 요청을 남긴적이 없습니다.";
    $result.innerText = "AI가 답변을 남긴적이 없습니다.";
  } else {
    write_history(detail);
    return [detail];
  }
}

// 불러온 내용을 html에 작성
function write_history(detail) {
  let ol_detail = document.createElement("ol");
  ol_detail.style.listStyleType = "number";

  detail.forEach((question, index) => {
    let li_detail = document.createElement("li");
    li_detail.innerText = question;
    li_detail.id = index;

    li_style(li_detail);

    li_detail.addEventListener("click", () => {
      let ai_history = JSON.parse(localStorage.getItem("ai"))[li_detail.id];
      let ai_code = document.createElement("pre");
      $result.innerText = "";
      ai_code.innerText = ai_history;
      $result.appendChild(ai_code);
    });
    ol_detail.appendChild(li_detail);
  });
  $question.appendChild(ol_detail);
}

load_history();

// 버튼클릭 시 초기화
$remove_btn.addEventListener("click", () => {
  if (confirm("정말 저장된 모든 기록을 초기화 시키겠습니까?")) {
    localStorage.removeItem("lang");
    localStorage.removeItem("method");
    localStorage.removeItem("detail");
    localStorage.removeItem("detail");
    localStorage.removeItem("ai");
    load_history();
  }
});

// 리스트 style 변경 모은함수
function li_style(li) {
  li.className = "mb-3";
  li.style.cursor = "pointer";
  li.style.listStyle = "decimal inside";
  li.addEventListener("mouseover", () => {
    li.style.color = "red";
  });
  li.addEventListener("mouseout", () => {
    li.style.color = "black";
  });
}
