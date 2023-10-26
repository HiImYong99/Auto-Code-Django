//서버와의 통신 js

import { data } from "./data.js";

let url = "https://estsoft-openai-api.jejucodingcamp.workers.dev/";
const $output_text = document.querySelector("#ai-answer");
export const $loading = document.querySelector("#loading");

//사용자에게 입력받은 요청을 data에 넣음
export const sendQuestion = (lang, method, detail) => {
  data.push({
    role: "user",
    content: `프로그래밍 언어는 ${lang}이고 ${detail}이걸 ${method} 해줘`,
  });
};

// api 통신 만약 성공시 printAnswer 함수 인자값에 받아온 결과값 전달
export const apiPost = async () => {
  await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
    redirect: "follow",
  })
    .then(res => res.json())
    .then(res => {
      printAnswer(res.choices[0].message.content);
    })
    .catch(err => {
      console.log(err);
    });
};

// api에게 받은 답변을 화면에 출력함
const printAnswer = async answer => {
  let pre = document.createElement("pre");
  let ai_arr = localStorage.getItem("ai")
    ? JSON.parse(localStorage.getItem("ai"))
    : [];
  pre.innerText = answer;
  ai_arr.push(answer);
  localStorage.setItem("ai", JSON.stringify(ai_arr));
  $loading.style.display = "none";
  const $existingPre = $output_text.querySelector("pre");
  if ($existingPre) {
    $output_text.removeChild($existingPre);
  }
  $output_text.appendChild(pre);
};
