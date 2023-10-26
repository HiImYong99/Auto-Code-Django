// 내 통계를 위한 js
const $use_count = document.querySelector("#use-count");
const $lang_count = document.querySelector("#lang-count");
const $method_count = document.querySelector("#method-count");
const $modal_btn = document.querySelector("#info-link");

// 배열에 저장된 lang값과 method값을 가져옴, 그 값들은 write_count 인자로 전달함
function load_count() {
  let lang = localStorage.getItem("lang")
    ? JSON.parse(localStorage.getItem("lang"))
    : [];

  let method = localStorage.getItem("method")
    ? JSON.parse(localStorage.getItem("method"))
    : [];

  if (lang.length === 0) {
    $use_count.innerText = "0회";
    $lang_count.innerText = "0회";
    $method_count.innerText = "0회";
  } else {
    write_count(lang, method);
    return [lang, method];
  }
}

// 저장한 데이터 정렬 및 최빈값 리턴
function getSortedArr(array) {
  // 출연 빈도 
  const counts = array.reduce((pv, cv) => {
    pv[cv] = (pv[cv] || 0) + 1;
    return pv;
  }, {});

  // 요소와 개수를 표현하는 배열 생성 
  const result = [];
  for (let key in counts) {
    result.push([key, counts[key]]);
  }

  // 출현 빈도별 정리
  result.sort((first, second) => {
    return second[1] - first[1];
  });

  return result;
}

// 정렬된 아이템과 최빈값을 html 문서에 작성
function write_count(lang, method) {
  let most_lang_name = getSortedArr(lang)[0][0];
  let most_lang_count = getSortedArr(lang)[0][1];
  let most_method_name = getSortedArr(method)[0][0];
  let most_method_count = getSortedArr(method)[0][1];

  $use_count.innerText = lang.length + "회";
  $lang_count.innerText = `${most_lang_name} ( ${most_lang_count}회 )`;
  $method_count.innerText = `${most_method_name} ( ${most_method_count}회 )`;
}

// 내 통계 버튼을 클릭할 시 새로고침
$modal_btn.addEventListener("click", () => {
  load_count();
});
