// 언어 목적 세부내용 로컬스토리지 관리위한 js

// 언어, 목적, 세부내용 로컬 스토리지에 저장
export function save_Item(lang, method, detail) {
  let lang_arr = load_Item()[0];
  let method_arr = load_Item()[1];
  let detail_arr = load_Item()[2];

  lang_arr.push(lang);
  method_arr.push(method);
  detail_arr.push(detail);

  localStorage.setItem("lang", JSON.stringify(lang_arr));
  localStorage.setItem("method", JSON.stringify(method_arr));
  localStorage.setItem("detail", JSON.stringify(detail_arr));
}

// 언어, 목적, 세부내용 로컬 스토리지에서 불러오기
export function load_Item() {
  let lang = localStorage.getItem("lang")
    ? JSON.parse(localStorage.getItem("lang"))
    : [];
  let method = localStorage.getItem("method")
    ? JSON.parse(localStorage.getItem("method"))
    : [];
  let detail = localStorage.getItem("detail")
    ? JSON.parse(localStorage.getItem("detail"))
    : [];

  return [lang, method, detail];
}
