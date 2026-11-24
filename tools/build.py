"""페이지 생성기.

tools/pages/*.html 의 본문에 공통 머리글 · 메뉴 · 상담 신청 · 바닥글을 붙여
사이트 루트에 같은 이름의 .html 파일을 만듭니다.

사용법:  python tools/build.py
각 페이지 파일 맨 위에는 아래 형식의 주석을 둡니다.
<!--title: 페이지 제목
desc: 검색 설명
nav: programs   (메뉴에서 강조할 페이지 이름, 홈은 home)
-->
"""
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "tools" / "pages"
SITE = "https://abroadstudy.co.kr"
PHONE, PHONE_TEL = "010-8241-2051", "01082412051"

NAV = [
    ("programs", "커리큘럼", "CURRICULUM"),
    ("process", "수업 진행", "PROCESS"),
    ("teachers", "코치진", "COACH"),
    ("samples", "샘플영상", "VIDEO"),
    ("price", "수강료", "PRICE"),
    ("news", "뉴스", "NEWS"),
    ("faq", "FAQ", "FAQ"),
]


def head(title, desc, path):
    url = SITE + ("/" if path == "index" else f"/{path}.html")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="naver-site-verification" content="02904e8faf9e8a803f1b1564c20affb8ec2e7da4" />
<meta name="google-site-verification" content="G6FB0mwcj3mD1-XkyL0RN1tQR17MfsDQ2It7sdVIkq8" />
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="theme-color" content="#0b0f1a">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23ffd400'/%3E%3Ctext x='16' y='21' font-size='13' font-weight='900' text-anchor='middle' fill='%230b0f1a' font-family='sans-serif'%3EAS%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.5.0/remixicon.min.css">
<link rel="stylesheet" href="/style.css">
</head>
<body>
"""


def header(active):
    links = "\n".join(
        f'      <a href="/{k}.html"{" class=\"on\"" if k == active else ""}>{label}</a>'
        for k, label, _ in NAV
    )
    return f"""
<header id="hdr">
  <div class="wrap nav">
    <a href="/" class="logo"><i class="ri-graduation-cap-fill"></i>어브로드스터디 국제학교과외</a>
    <nav class="menu" id="menu">
{links}
      <a href="#apply" class="cta">무료 테스트</a>
    </nav>
    <button class="burger" id="burger" aria-label="메뉴"><i class="ri-menu-line"></i></button>
  </div>
</header>
"""


def more(active):
    items = [(k, label, en) for k, label, en in NAV if k != active] + [("", "메인으로", "HOME")]
    cards = "\n".join(
        f'      <a href="/{k + ".html" if k else ""}" class="more-card"><small>{en}</small><b>{label}</b><i class="ri-arrow-right-up-line"></i></a>'
        for k, label, en in items
    )
    return f"""
<section class="more">
  <div class="wrap">
    <div class="head"><span class="pill dk">MORE</span><h2>다른 안내 보기</h2></div>
    <div class="more-grid">
{cards}
    </div>
  </div>
</section>
"""


APPLY = f"""
<section id="apply" class="dark">
  <div class="wrap apply">
    <div>
      <span class="pill">FREE TEST CLASS</span>
      <h2>먼저 <em>10~15분 무료 테스트</em>부터<br>받아 보세요</h2>
      <p>학교 · 학년 · 과목만 알려 주시면 맞는 코치를 찾아 무료 테스트 수업 일정을 잡아 드려요. 상담과 테스트 수업 모두 비용이 없습니다.</p>
      <div class="info">
        <a href="tel:{PHONE_TEL}"><i class="ri-phone-fill"></i><span><b>전화 상담</b><span class="big">{PHONE}</span> · 평일 10:00 – 19:00</span></a>
        <div><i class="ri-time-line"></i><span><b>회신 안내</b>신청서를 남기시면 영업일 기준 24시간 안에 담당자가 연락드려요.</span></div>
        <div><i class="ri-user-follow-line"></i><span><b>부담 없는 시작</b>테스트 후 코치 변경 요청 가능 · 추가 교재비 · 관리비 없음</span></div>
      </div>
    </div>
    <form id="applyForm" novalidate>
      <div class="form-head"><h3>무료 테스트 수업 신청</h3><p>아래 정보만 남겨 주시면 바로 연락드릴게요.</p></div>
      <label>학생 이름 *<input name="name" required autocomplete="off"></label>
      <label>연락처 *<input name="phone" type="tel" required placeholder="010-0000-0000"></label>
      <label>학년 *
        <select name="grade" required>
          <option value="">선택</option>
          <option>G1</option><option>G2</option><option>G3</option><option>G4</option><option>G5</option><option>G6</option>
          <option>G7</option><option>G8</option><option>G9</option><option>G10</option><option>G11</option><option>G12</option>
          <option>기타 · 편입 준비</option>
        </select>
      </label>
      <label>희망 과정 *
        <select name="course" required>
          <option value="">선택</option>
          <option>IB (MYP · DP)</option><option>AP</option><option>IGCSE · A-Level</option><option>SAT · 공인시험</option>
          <option>국제학교 수학</option><option>영어 에세이 · 리서치</option><option>영어 토론 · 발표 (MUN)</option>
          <option>미국교과서 · 과학</option><option>편입 · 유학 준비</option><option>아직 정하지 못했어요</option>
        </select>
      </label>
      <label>재학 중인 학교<input name="school"></label>
      <label>거주 지역 · 시간대<input name="region" placeholder="예) 서울 / 싱가포르"></label>
      <label class="full">희망 수업
        <select name="plan">
          <option>상담 후 결정</option>
          <option>주 2회 · 1시간 (월 480,000원)</option>
          <option>주 2회 · 90분 (월 720,000원)</option>
        </select>
      </label>
      <label class="full">상담 내용<textarea name="memo" placeholder="궁금한 점이나 원하는 수업 시간을 적어 주세요."></textarea></label>
      <label class="agree full"><input type="checkbox" name="agree"> 상담을 위한 개인정보(이름, 연락처, 학년, 상담 내용) 수집 · 이용에 동의합니다. 수집한 정보는 상담 목적으로만 사용하며 1년 후 파기합니다.</label>
      <p class="form-msg" id="formMsg" role="status"></p>
      <button type="submit" class="btn btn-y full">무료 테스트 수업 신청하기 <i class="ri-arrow-right-line"></i></button>
    </form>
  </div>
</section>
"""


def footer():
    links = "".join(f'<a href="/{k}.html">{label}</a>' for k, label, _ in NAV)
    return f"""
<footer>
  <div class="wrap">
    <div class="f-grid">
      <div class="f-brand">
        <a href="/" class="logo"><i class="ri-graduation-cap-fill"></i>어브로드스터디 국제학교과외</a>
        <p>IB · AP · IGCSE · A-Level · SAT부터 미국교과서 수학과 영어 에세이까지, 국제학교 커리큘럼에 맞춘 1:1 실시간 온라인 과외입니다.</p>
      </div>
      <div class="f-col"><h4>커리큘럼</h4><a href="/programs.html">IB (MYP · DP)</a><a href="/programs.html">AP</a><a href="/programs.html">IGCSE · A-Level</a><a href="/programs.html">국제학교 수학</a><a href="/programs.html">SAT · 공인시험</a></div>
      <div class="f-col"><h4>안내</h4>{links}</div>
      <div class="f-col"><h4>상담</h4><a href="tel:{PHONE_TEL}">전화 {PHONE}</a><a>평일 10:00 – 19:00</a><a href="#apply">무료 테스트 신청</a><a href="#privacy">개인정보 수집 · 이용</a></div>
    </div>
    <p class="legal" id="privacy">개인정보 수집 · 이용 안내: 상담 신청 시 이름, 연락처, 학년, 학교, 거주 지역, 상담 내용을 수집하며 상담 진행 목적으로만 이용합니다. 보유 기간은 1년이며 기간이 지나면 지체 없이 파기합니다.<br>© 2026 어브로드스터디 국제학교과외. 국제학교 1:1 실시간 온라인 과외.</p>
  </div>
</footer>

<div class="bar">
  <div class="wrap">
    <div class="t"><i class="ri-graduation-cap-fill"></i><span>국제학교 1:1 과외 상담</span><small>평일 10:00 – 19:00</small></div>
    <div class="b">
      <a href="tel:{PHONE_TEL}" class="btn btn-line"><i class="ri-phone-fill"></i> {PHONE}</a>
      <a href="#apply" class="btn btn-y">무료 테스트</a>
    </div>
  </div>
</div>

<script src="/site.js"></script>
</body>
</html>
"""


def build():
    built = []
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text(encoding="utf-8")
        m = re.match(r"<!--(.*?)-->\s*", text, re.S)
        meta = dict(
            line.split(":", 1) for line in m.group(1).strip().splitlines() if ":" in line
        )
        meta = {k.strip(): v.strip() for k, v in meta.items()}
        body = text[m.end():]
        name = src.stem
        if name != "index":
            label = next((l for k, l, _ in NAV if k == name), "")
            body = body.replace(
                '<section class="page-hero">\n  <div class="wrap">',
                '<section class="page-hero">\n  <div class="wrap">\n'
                '    <div class="crumb"><a href="/">홈</a> › <b>' + label + "</b></div>",
                1,
            )
            body = re.sub(
                r'<span class="eyebrow">([A-Z ]+?) · ',
                lambda m: '<span class="eyebrow"><em>' + m.group(1).title() + "</em>",
                body,
            )
        html = (
            head(meta["title"], meta["desc"], name)
            + header(meta.get("nav", name))
            + '\n<main id="top">\n'
            + body
            + (more(name) if name != "index" else "")
            + APPLY
            + "</main>\n"
            + footer()
        )
        (ROOT / f"{name}.html").write_text(html, encoding="utf-8")
        built.append(name)

    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>{SITE}{'/' if n == 'index' else '/' + n + '.html'}</loc><lastmod>{today}</lastmod></url>"
        for n in built
    )
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
        encoding="utf-8",
    )
    print("built:", ", ".join(built))


if __name__ == "__main__":
    build()
