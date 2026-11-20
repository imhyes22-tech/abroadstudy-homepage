// 상담 신청을 받을 주소 (Formspree 등). 비어 있으면 문자(SMS) 앱으로 신청 내용을 보냅니다.
const FORM_ENDPOINT = '';
const PHONE = '01082412051';

// 헤더: 스크롤하면 배경 채우기
const hdr = document.getElementById('hdr');
const onScroll = () => hdr.classList.toggle('solid', scrollY > 40);
addEventListener('scroll', onScroll, { passive: true }); onScroll();

// 모바일 메뉴
const menu = document.getElementById('menu');
document.getElementById('burger').addEventListener('click', () => {
  hdr.classList.toggle('open', menu.classList.toggle('open'));
});
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => { menu.classList.remove('open'); hdr.classList.remove('open'); }));

// 학교 이름 흐름띠: 끊김 없이 돌도록 한 번 복제
const track = document.getElementById('track');
track.innerHTML += track.innerHTML;

// 지역별 학교 탭
const SCHOOLS = {
  '서울 · 경기': ['서울외국인학교 (SFS)', '용산국제학교 (YISS)', '드와이트외국인학교', '덜위치칼리지서울영국학교', '한국외국인학교 (KIS)', '서울국제학교 (SIS)', '경기수원외국인학교 (GSIS)', '아시아퍼시픽국제외국인학교 (APIS)', '한국켄트외국인학교'],
  '인천 · 송도': ['채드윅 송도국제학교', '칼빈매니토바국제학교'],
  '제주': ['NLCS Jeju', '브랭섬홀 아시아 (BHA)', 'KIS 제주', 'SJA 제주'],
  '지방': ['대구국제학교 (DIS)', '부산외국인학교 (BFS)', '부산국제외국인학교 (ISB)', '대전외국인학교 (TCIS)', '광주외국인학교'],
  '중국 · 홍콩': ['SCIS 상하이', 'BCIS 베이징', 'Shanghai American School', 'HKIS 홍콩'],
  '동남아': ['싱가포르 SAS', 'UWCSEA 싱가포르', '하노이 BIS', 'UNIS Hanoi', 'SSIS 호치민', 'ISKL 쿠알라룸푸르', 'JIS 자카르타', 'ISB 방콕', 'NIST 방콕', 'ISM 마닐라'],
  '일본 · 중동': ['ASIJ 도쿄', 'GEMS 웰링턴 (두바이)', '두바이 · 아부다비 국제학교'],
  '미주 · 유럽': ['미국 공립 · 사립학교', '캐나다 공립 · 사립학교', '영국 · 유럽 국제학교'],
};
const tabs = document.getElementById('tabs');
const panel = document.getElementById('panel');
const showRegion = (name) => {
  tabs.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.textContent === name));
  panel.innerHTML = `<h3>${name}</h3><div class="chips">${SCHOOLS[name].map(s => `<span>${s}</span>`).join('')}</div>`;
};
Object.keys(SCHOOLS).forEach(name => {
  const b = document.createElement('button');
  b.type = 'button'; b.textContent = name;
  b.addEventListener('click', () => showRegion(name));
  tabs.appendChild(b);
});
showRegion(Object.keys(SCHOOLS)[0]);

// 상담 신청
const form = document.getElementById('applyForm');
const msg = document.getElementById('formMsg');
const show = (type, text) => { msg.className = 'form-msg ' + type; msg.textContent = text; };

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const f = form.elements;
  if (!f.name.value.trim() || !f.phone.value.trim() || !f.grade.value || !f.course.value) {
    return show('err', '이름, 연락처, 학년, 희망 과정을 입력해 주세요.');
  }
  if (!f.agree.checked) return show('err', '개인정보 수집 · 이용에 동의해 주세요.');

  if (FORM_ENDPOINT) {
    const btn = form.querySelector('button[type=submit]');
    btn.disabled = true;
    try {
      const res = await fetch(FORM_ENDPOINT, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
      if (!res.ok) throw new Error(res.status);
      form.reset();
      show('ok', '신청이 접수됐어요. 영업일 기준 24시간 안에 연락드릴게요.');
    } catch {
      show('err', `전송에 실패했어요. ${PHONE.replace(/(\d{3})(\d{4})(\d{4})/, '$1-$2-$3')}로 전화 주시면 바로 상담해 드려요.`);
    } finally { btn.disabled = false; }
    return;
  }

  // 접수 서버가 없을 때: 문자 앱에 신청 내용을 채워서 엽니다.
  const body = [
    '[어브로드스터디 무료 테스트 신청]',
    `이름: ${f.name.value}`, `연락처: ${f.phone.value}`, `학년: ${f.grade.value}`, `과정: ${f.course.value}`,
    f.school.value && `학교: ${f.school.value}`, f.region.value && `지역: ${f.region.value}`,
    `희망: ${f.plan.value}`, f.memo.value && `내용: ${f.memo.value}`
  ].filter(Boolean).join('\n');
  const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
  if (isMobile) {
    const sep = /iPhone|iPad|iPod/i.test(navigator.userAgent) ? '&' : '?';
    location.href = `sms:${PHONE}${sep}body=${encodeURIComponent(body)}`;
    show('ok', '문자 앱이 열리면 전송 버튼을 눌러 주세요.');
  } else {
    show('err', 'PC에서는 접수가 어려워요. 010-8241-2051로 전화나 문자 주시면 바로 상담해 드려요.');
  }
});
