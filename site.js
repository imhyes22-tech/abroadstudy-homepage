// 상담 신청을 받을 주소 (Formspree 등). 비어 있으면 문자(SMS) 앱으로 신청 내용을 보냅니다.
const FORM_ENDPOINT = '';
const PHONE = '01082412051';

// 모바일 메뉴
const menu = document.getElementById('menu');
document.getElementById('burger').addEventListener('click', () => menu.classList.toggle('open'));
menu.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));

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
