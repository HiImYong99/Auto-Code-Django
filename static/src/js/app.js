import { save_Item } from "./local-storage.js";
import { sendQuestion, apiPost, $loading } from "./api.js";

const $btn = document.querySelector("#submit-btn");
const $form = document.querySelector("#user-form");
const $input_lang = document.querySelector("#language");
const $input_method = document.querySelector("#method");
const $input_text = document.querySelector("#detail-content");

// 요청버튼 클릭 시 발생
$form.addEventListener("submit", e => {
  e.preventDefault();

  const lang_value = $input_lang.options[$input_lang.selectedIndex].value;
  const method_value = $input_method.options[$input_method.selectedIndex].value;
  const detail_value = $input_text.value;

  alert("요청되었습니다. 잠시만 기다려주세요.");
  loading_appear();
  sendQuestion(lang_value, method_value, detail_value);
  apiPost();
  save_Item(lang_value, method_value, detail_value);
});

//실행해보기 버튼 클릭 시 발생
$btn.addEventListener("click", e => {
  const openNewWindow = window.open("about:blank");
  openNewWindow.location.href =
    "https://www.ryugod.com/pages/ide/" +
    $input_lang.options[$input_lang.selectedIndex].value;
});

// spinner
function loading_appear() {
  const $example = document.querySelector("#explain");
  $example.style.display = "none";
  $loading.style.display = "block";
}
